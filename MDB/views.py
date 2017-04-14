from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.renderers import JSONRenderer
from django.shortcuts import redirect

import logging
import json
import forms
import models
import serializers
import tasks

from syllextract import extract
from datetime import datetime
from pytz import timezone

logging.basicConfig(
    filename='views.log',
    level=logging.DEBUG,
    format='%(asctime)s %(message)s',
    datefmt='%m/%d/%Y %I:%M:%S %p'
)

###################### RENDERS ##################
def landing(request):
    #normally this will rendeer the landing page. skipping that for now. forwarding to login.
    return render(request, 'landing.html')

def thankyou(request):
    email = request.POST.get('email')

    if email:
        print email
        models.NewsReceiver.objects.create(email=email)
    return render(request, 'thankyou.html')

def login(request):
    return render(request, 'register-login.html')

@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

@login_required
def dashboard(request):
    user = request.user
    courses = [c.course_code for c in list(user.course_set.all())]

    #SERIALIZE EVENT TODO: MAKE A REAL SERIALIZER
    events = []
    for e in list(user.event_set.all().order_by('due_date')):
        event = {
            "id": e.id,
            "name": e.name,
            "due_date": e.due_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
            "course": e.course.course_code
        }
        events.append(event)

    notes = []
    for n in list(user.note_set.all()):
        note = {
            "id": n.id,
            "title": n.title,
            "text": n.text
        }
        notes.append(note)
    context = {
        "user": user,
        "courses": json.dumps(courses),
        "events": json.dumps(events),
        "notes": json.dumps(notes)
    }

    return render(request, 'dashboard.html', context)

def signup(request):
    form = forms.SignupForm()
    return render(request, 'create_account.html', {"form": form})

def verify_number(request):
    return render(request, 'verify_number.html')

@login_required
def add_course(request):
    return render(request, 'add_course.html')

@login_required
def amend_course(request):
    #Results from Uploading Syllabus
    events = {}
    found_params = {}
    if request.session.get('found_params'):
        found_params = request.session.get('found_params')
        del request.session['found_params']

        events = found_params["events"]
        del found_params["events"]
        print events
    #Manual Config
    else:
        try:
            found_params = dict(request.POST)
            if found_params['csrfmiddlewaretoken']:
                del found_params['csrfmiddlewaretoken']
            for key, value in found_params.iteritems():
                found_params[key] = value[0]
        except:
            #everything is borken so just return empty info so it doens't crash
            found_params = {}
            events = {}

    return render(request, 'confirm_course.html', {"found_params": found_params, "events": events})

@login_required
def new_event(request):
    user = request.user
    course_query = user.course_set.all()
    course_codes = [(course.id, course.course_code) for course in list(course_query)]

    return render(request, 'new_event.html', {"course_list": course_codes})


#################### ACTIONS ###############
def login_action(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = email, password = password)

    if user:
        auth.login(request, user)
        return HttpResponseRedirect('/home')

    else:
        request.path = "/login"
        # messages.add_message(request, {"message": "Invalid Login"})
        return HttpResponseRedirect(request.path, {"message": "Invalid Login"})

@login_required
def syllabi_upload_action(request):
     if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        found_params = extract.main(myfile)

        request.session['found_params'] = found_params
        return HttpResponseRedirect('/add_course/amend_course/')

@api_view(['POST'])
def signup_action(request):
    print request.data
    serialized = serializers.MDBUserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        # create and login user with empty phone number (needs validation first)
        user = auth.authenticate(username=request.data['email'], password=request.data['password'])
        if user:
            auth.login(request, user)
        return HttpResponseRedirect('/verify_number/')
    else:
        return HttpResponseRedirect('/signup/')

@login_required
@api_view(['POST'])
def submit_number_action(request):
    user = request.user
    user.phone_number=request.POST.get('number')
    user.save()

    try:
        code = tasks.validate_number(request.POST.get('number'))
        return HttpResponse(str(code))
    except:
        return HttpResponse('Number already in use', status=400)


@login_required
def check_verified_action(request):
    user = request.user
    if tasks.number_is_validated(user.phone_number):
        user.number_verified = True
        user.save()
        return HttpResponseRedirect('/add_course/')
    else:
        return HttpResponseRedirect('/verify_number/', {"message": "Verification Failed"})

@login_required
@api_view(['POST'])
def new_event_action(request):
    request.data["owner"] = request.user.id
    request.data["course"] = request.user.course_set.get(course_code=request.data["course"]).id

    serialized = serializers.EventSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        print serialized.data
        return HttpResponse(json.dumps(serialized.data), status=201)
    else:
        return HttpResponseRedirect('/new_event/')

@login_required
@api_view(['POST'])
def new_note_action(request):
    request.data["owner"] = request.user.id

    serialized = serializers.NoteSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
        return HttpResponse(json.dumps(serialized.data), status=201)
    else:
        return HttpResponse(status=500)


@login_required
@api_view(['POST'])
def confirm_course_action(request):
    course_info = dict(json.loads(request.data['course_info']))
    events = list(json.loads(request.data['events']))

    print course_info
    #TODO: A serializer SHOULD work for this....but doesn't
    try:
        course = models.Course.objects.create(
            course_code=course_info['course_code'],
            instructor_name=course_info['instructor_name'],
            instructor_email=course_info['instructor_email'],
            instructor_office=course_info['instructor_office']
        )
    except:
        logging.debug("ERROR User: {0} -- Course Info: {0}".format(request.user, course_info))
        return HttpResponse("Problem with course info", status=500)

    try:
        for event in events:
            due_date = datetime.strptime(event['due_date'], '%Y-%m-%d')
            print due_date
            psf = timezone('US/Pacific')
            time = psf.localize(due_date)
            event = models.Event.objects.create(
                owner=request.user,
                name=event["name"],
                priority=event["priority"],
                due_date=time,
                course=course
            )
    except:
        logging.debug("ERROR User: {0} -- Events: {1}".format(request.user, events))
        return HttpResponse("Problem with event info", status=500)

    course.students.add(request.user)

    return HttpResponse(status=201)

@login_required
@api_view(['DELETE'])
def delete_event(request):
    # try:
    eventID = request.data['eventID'][0]
    models.Event.objects.get(id=eventID).delete()

    return HttpResponse(status=200)
    # except:
    #     return HttpResponse(status=500)

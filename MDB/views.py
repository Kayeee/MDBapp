from django.shortcuts import render
from django.contrib import auth
from django.http import HttpResponse, Http404, HttpResponseRedirect
from rest_framework.decorators import api_view

import forms
import models
import serializers
from syllextract import extract


###################### RENDERS ##################
def landing(request):
    #normally this will rendeer the landing page. skipping that for now. forwarding to login.
    return HttpResponseRedirect('/login/')

def login(request):
    return render(request, 'login.html')

def dashboard(request):
    user = request.user

    return render(request, 'dashboard.html')

def signup(request):
    form = forms.SignupForm()
    return render(request, 'signup.html', {"form": form})

def add_course(request):
    return render(request, 'add_course.html')

def amend_course(request):
    found_params = request.session.get('found_params')
    events = found_params["events"]
    del found_params["events"]

    return render(request, 'amend_course.html', {"found_params": found_params, "events": events})

#################### ACTIONS ###############
def login_action(request):
    email = request.POST.get('email', '')
    password = request.POST.get('password', '')
    user = auth.authenticate(username = email, password = password)

    print email, password

    if user:
        auth.login(request, user)
        return HttpResponseRedirect('/home')

    else:
        request.path = "/login"
        messages.add_message(request, messages.INFO, 'Invalid Login')
        return HttpResponseRedirect(request.path)

def syllabi_upload_action(request):
     if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        found_params = extract.main(myfile)

        request.session['found_params'] = found_params
        return HttpResponseRedirect('/add_course/amend_course')

@api_view(['POST'])
def signup_action(request):
    serialized = serializers.MDBUserSerializer(data=request.data)
    if serialized.is_valid():
        serialized.save()
    return HttpResponseRedirect('/add_course/')

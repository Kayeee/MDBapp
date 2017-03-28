from __future__ import absolute_import


import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyDigitalBackpack2.settings")

import django
django.setup()

from django.conf import settings
from celery import shared_task, Celery
from twilio.rest import TwilioRestClient

import datetime
import pytz

from .models import Event, MDBUser


twilio_account_sid = "AC3fcf677d16b6381be0eae457cc471911"
twilio_auth_token  = "c5d209b1641664585658831b1a6e67e5"
TWILIO_NUMBER = '+14805269460'
client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

app = Celery('event_worker', backend='amqp', broker='amqp://Kevin:ASUi3dea@localhost/pi_env')

@shared_task
def send_sms_reminder(event_id, owner_id):

    try:
        event = Event.objects.get(pk=event_id)
        owner = MDBUser.objects.get(pk=owner_id)
    except Event.DoesNotExist:
        print "Either event or owner id does not exist. Aborting..."
        return

    body = 'Hi {0}. {1} is due on {2} at {3} '.format(
        owner.first_name,
        event.name,
        event.due_date.strftime("%A"),
        event.due_date.strftime("%-I:%M %p")
    )

    message = client.messages.create(
        body=body,
        to=owner.phone_number,
        from_=TWILIO_NUMBER
    )

def validate_number(phone_number):
    response = client.caller_ids.validate(phone_number=phone_number, call_delay=5)
    # # response = {u'phone_number': u'+14806068899',
    # u'validation_code': u'585169',
    # u'friendly_name': None, u'call_sid': u'CAcf6cb2d1cdd6effe866dd892d6adb7f2',
    #  u'account_sid': u'AC3fcf677d16b6381be0eae457cc471911'}
    return response['validation_code']

def number_is_validated(phone_number):
    ids = client.caller_ids.list(phone_number=phone_number)
    if ids:
        return True
    else:
        return False

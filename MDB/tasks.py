from __future__ import absolute_import

from celery import shared_task, Celery
from django.conf import settings
from twilio.rest import TwilioRestClient

import datetime

#from .models import Event

twilio_account_sid = "AC3fcf677d16b6381be0eae457cc471911"
twilio_auth_token  = "c5d209b1641664585658831b1a6e67e5"
client = TwilioRestClient(twilio_account_sid, twilio_auth_token)

app = Celery('event_worker', backend='amqp', broker='amqp://Kevin:ASUi3dea@localhost/pi_env')

@shared_task
def send_sms_reminder(event_id, owner_id):

    try:
        event = Event.objects.get(pk=event_id)
        owner = MDBUser.objects.get(pk=owner_id)
    except Event.DoesNotExist:
        return

    event_time = event.due_date
    days_to_event = (event.due_date - datetime.datetime.now()).days
    body = 'Hi {0}. {1} is due in {2} days'.format(
        owner.first_name,
        event.name,
        str(days_to_event),
    )

    message = client.messages.create(
        body=body,
        to=owner.phone_number,
        from_=settings.TWILIO_NUMBER,
    )

@shared_task
def test_send_sms():
    TWILIO_NUMBER = '+14805269460'
    message = client.messages.create(body="Hello", to="+14794200552", from_=TWILIO_NUMBER)

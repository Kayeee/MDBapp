from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

import datetime
from pytz import timezone

# Create your models here.
class MDBUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, password, phone_number="+1",):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, password, phone_number="+1",):


        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number = phone_number,
 	        password=password,
        )
        user.is_admin = True
        user.set_password(password)
        user.save(using=self._db)

        return user


class MDBUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField(default='2016-1-1')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15, blank=True)
    number_verified = models.BooleanField(default=False)

    objects = MDBUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'first_name', 'last_name', 'date_of_birth']

    def get_full_name(self):
        return self.first_name + " " + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

# class School(models.Model):
#     pass

class Course(models.Model):
    #course_code is the 3 letter id and 3 digit number (SER 505)
    course_code = models.CharField(max_length=50)
    students = models.ManyToManyField(MDBUser, related_name='course_set')
    instructor_name = models.CharField(max_length=50, default="")
    instructor_email = models.EmailField(
        verbose_name='Instructor email',
        max_length=255,
        default="",
    )
    instructor_office  = models.CharField(max_length=50, default="")

    def __str__(self):
        return self.course_code


class Event(models.Model):
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    PRIORITY_CHOICES = (
        (LOW, 0),
        (MEDIUM, 1),
        (HIGH, 2),
    )

    priority = models.PositiveSmallIntegerField(
        choices=PRIORITY_CHOICES,
        default=LOW,
    )

    name = models.CharField(max_length=50, default="My Event")
    due_date = models.DateTimeField(blank=False)
    note = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='event_set'
    )
    owner = models.ForeignKey(
        MDBUser,
        on_delete=models.CASCADE,
        related_name='event_set'
    )

    #fields not visible to user
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def success_url(self):
        return reverse('add_course')

    def _make_date(self, diff):
        #convert to UTC time
        new_date = self.due_date.astimezone(timezone('UTC'))
        new_date = new_date - datetime.timedelta(days=diff)

        print "New date: {0}".format(new_date)
        return new_date

    def schedule_reminder(self):
        from tasks import send_sms_reminder
        result_ids = []

        #make 1 day reminder
        result_ids.append(send_sms_reminder.apply_async(args=[self.pk, self.owner.pk], eta=self._make_date(1)))

        print "Priority: {0}".format(self.priority)
        #make 3 day reminder
        if self.priority >= 1:
            result_ids.append(send_sms_reminder.apply_async(args=[self.pk, self.owner.pk], eta=self._make_date(3)))

        #make 7 day reminder:
        if self.priority >= 2:
            result_ids.append(send_sms_reminder.apply_async(args=[self.pk, self.owner.pk], eta=self._make_date(7)))

        return result_ids


    def save(self, *args, **kargs):
        from tasks import app

        for task in list(self.task_set.all()):
            app.control.revoke(task.celery_id)
            task.delete()

        #TODO: Fix Timezone stuff.
        print self.due_date.tzinfo

        #let the database know of the timezone that the entered date was
        #TODO:The timezone should be depending on the user
        self.due_date = self.due_date.replace(tzinfo=timezone('US/Pacific'))
        #for some reason it is an hour off
        self.due_date = self.due_date - datetime.timedelta(hours=1) + datetime.timedelta(minutes=7)

        super(Event, self).save(*args, **kargs)

        #super before so we know self.pk
        result_ids = self.schedule_reminder()
        for result_id in result_ids:
            self.task_set.add(Task.objects.create(celery_id=result_id, event_id=self.pk))


class NewsReceiver(models.Model):
    email = models.EmailField()

    def __str__(self):
        return self.email

class Task(models.Model):
    celery_id = models.CharField(max_length=50, blank=True, editable=False)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='task_set')

    def __str__(self):
        return self.celery_id

class Note(models.Model):
    owner = models.ForeignKey(
        MDBUser,
        on_delete=models.CASCADE,
        related_name='note_set'
    )
    text = models.TextField(blank=False)
    title = models.CharField(max_length=40, blank=False, default="Title")

from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

import datetime

# Create your models here.
class MDBUserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, date_of_birth, phone_number, password):

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number=phone_number,
        )

        print "here"
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, date_of_birth, phone_number, password):

        user = self.create_user(
            email,
            first_name=first_name,
            last_name=last_name,
            date_of_birth=date_of_birth,
            phone_number = phone_number,
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
    phone_number = models.CharField(max_length=15)

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
    students = models.ManyToManyField(MDBUser, related_name='courses_set')
    instructor_name = models.CharField(max_length=50, default="")
    instructor_email = models.EmailField(
        verbose_name='Instructor email',
        max_length=255,
        default="",
    )
    instructor_office  = models.CharField(max_length=50, default="")

from .tasks import send_sms_reminder, app

class Event(models.Model):
    name = models.CharField(max_length=50, default="My Event")
    due_date = models.DateTimeField(default=(datetime.datetime.now() + datetime.timedelta(days=7)))
    note = models.TextField()
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='event_set'
    )
    owner = models.ForeignKey(
        MDBUser,
        on_delete=models.CASCADE,
        related_name='events_set'
    )

    #fields not visible to user
    task_id = models.CharField(max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def success_url(self):
        return reverse('add_course')

    def schedule_reminder(self):
        reminder_time = self.due_date - datetime.timedelta(hours=23, minutes=59)


        result = send_sms_reminder.apply_async(args=[self.pk, self.owner.pk], eta=reminder_time)

        print result.id
        return result.id

    def save(self, *args, **kargs):
        print "here 1"
        if self.task_id:
            app.control.revoke(self.task_id)

        print "here 2"
        super(Event, self).save(*args, **kargs)
        print "here 3"
        self.task_id = self.schedule_reminder()
        print self.task_id
        super(Event, self).save(*args, **kargs)

from rest_framework import serializers
from django.contrib.auth import get_user_model

from models import *


class MDBUserSerializer(serializers.ModelSerializer):
    courses_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Course.objects.all()
    )
    events_set = serializers.PrimaryKeyRelatedField(
        many=True,
        required=False,
        queryset=Event.objects.all()
    )

    class Meta:
        model = MDBUser
        fields = ('id', 'email', 'is_active', 'is_admin', 'first_name', 'last_name',
            'date_of_birth', 'phone_number', 'courses_set', 'events_set', 'password')

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
        )

        return user

class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ('course_code', 'instructor_name', 'instructor_email', 'instructor_office')

    # def create(self, validated_data):
    #     print validated_data
    #     course = Course.objects.create(
    #
    #         course_code=validated_data['course_code'],
    #         instructor_name=validated_data['instructor_name'],
    #         instructor_email=validated_data['instructor_email'],
    #         instructor_office=validated_data['instructor_office']
    #     )
    #     return course


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields =('name', 'due_date', 'course', 'owner', 'priority')

    def create(self, validated_data):
        event = Event.objects.create(
            name=validated_data['name'],
            due_date=validated_data['due_date'],
            course=validated_data['course'],
            owner=validated_data['owner'],
            priority=validated_data['priority']
        )
        return event


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields =('title', 'text', 'owner')

    def create(self, validated_data):
        note = Note.objects.create(
            title=validated_data['title'],
            text=validated_data['text'],
            owner=validated_data['owner']
        )
        return note

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
            phone_number=validated_data['phone_number'],
            date_of_birth=validated_data['date_of_birth'],
            password=validated_data['password'],
        )

        return user

class CourseSerializer(serializers.ModelSerializer):
    students = serializers.ReadOnlyField(source='students.all()')

    class Meta:
        model = Course
        fields = ('course_code', 'students', 'instructor_name', 'instructor_email',
            'instructor_office')

class EventSerializer(serializers.ModelSerializer):
    #course = serializers.ReadOnlyField(source="course.course_code")
    #owner = serializers.ReadOnlyField(source="owner.username")

    class Meta:
        model = Event
        fields =('name', 'due_date', 'note', 'course', 'owner')

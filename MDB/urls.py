from django.conf.urls import include, url
from django.contrib import admin

import views, apiViews

urlpatterns = [
    # views
    url(r'^$', views.landing, name='landing'),
    url(r'^thankyou/', views.thankyou, name='thankyou'),
    url(r'^login/', views.login, name='login'),
    url(r'^logout/', views.logout, name='logout'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^verify_number/', views.verify_number, name='verify_number'),
    url(r'^add_course/$', views.add_course, name='add_course'),
    url(r'^add_course/amend_course', views.amend_course, name='amend_course'),
    url(r'^home/', views.dashboard, name='dashboard'),
    url(r'^new_event/', views.new_event, name='new_event'),

    #actions
    url(r'^login_action/', views.login_action, name='login_action'),
    url(r'^signup_action/', views.signup_action, name='signup_action'),
    url(r'^submit_number_action/', views.submit_number_action, name='submit_number_action'),
    url(r'^syllabi_upload_action/', views.syllabi_upload_action, name='syllabi_upload_action'),
    url(r'^confirm_course_action/', views.confirm_course_action, name='confirm_course_action'),
    url(r'^new_event_action/', views.new_event_action, name='new_event_action'),
    url(r'^check_verified_action/', views.check_verified_action, name='check_verified_action'),
    url(r'^new_note_action/', views.new_note_action, name='new_note_action'),
    url(r'^delete_event/', views.delete_event, name='delete_event'),
    url(r'^delete_course/', views.delete_course, name='delete_course'),

    #class views for API
    url(r'^users/$', apiViews.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', apiViews.UserDetail.as_view()),
    url(r'^courses/$', apiViews.CourseList.as_view()),
    url(r'^courses/(?P<pk>[0-9]+)/$', apiViews.CourseDetail.as_view()),
    url(r'^events/$', apiViews.EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', apiViews.EventDetail.as_view()),

]

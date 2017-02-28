from django.conf.urls import include, url
from django.contrib import admin

import views, apiViews

urlpatterns = [
    # views
    url(r'^$', views.landing, name='landing'),
    url(r'^login/', views.login, name='login'),
    url(r'^signup/', views.signup, name='signup'),
    url(r'^add_course/$', views.add_course, name='add_course'),
    url(r'^add_course/amend_course', views.amend_course, name='amend_course'),
    url(r'^home/', views.dashboard, name='dashboard'),

    #actions
    url(r'^login_action/', views.login_action, name='login_action'),
    url(r'^signup_action/', views.signup_action, name='signup_action'),
    url(r'^syllabi_upload_action/', views.syllabi_upload_action, name='syllabi_upload_action'),

    #class views for API
    url(r'^users/$', apiViews.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', apiViews.UserDetail.as_view()),
    url(r'^courses/$', apiViews.CourseList.as_view()),
    url(r'^courses/(?P<pk>[0-9]+)/$', apiViews.CourseDetail.as_view()),
    url(r'^events/$', apiViews.EventList.as_view()),
    url(r'^events/(?P<pk>[0-9]+)/$', apiViews.EventDetail.as_view()),

]

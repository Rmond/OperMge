#!/usr/local/bin/python2.7
# encoding: utf-8

from django.conf.urls import url

import views

urlpatterns = [
    url(r'^hostidlechk',views.hostidle_check,name="hostidle_check"),
    url(r'^hostipchk',views.hostip_check,name="hostip_check"),
]
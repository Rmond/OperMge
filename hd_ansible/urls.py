#!/usr/local/bin/python2.7
# encoding: utf-8

from django.conf.urls import url

import views
from software import softview


urlpatterns = [
    url(r'^tomcat/projectdev',views.ProjectDev),
    url(r'^tomcat/rollback',views.RollBack),
    url(r'^tomcat/grouphostget',views.GroupHostGet),
    url(r'^tomcat/multiselect',views.MultiSelect),
    url(r'^inventory/inventorymge',views.InventoryMge),
    url(r'^software/softselect$',softview.software_select),
    url(r'^software/install$',softview.software_install),
    url(r'^software/update$',softview.software_update),
    url(r'^software/installed$',softview.software_installed),
    url(r'^software/updated$',softview.software_updated),
    url(r'^software/grouphostget',softview.grouphost_get),
    url(r'^software/ugrouphostget',softview.u_grouphost_get),
    url(r'^yum/manage/(?P<option>\w+)$',views.yum_manage,),
    url(r'^yum/execute/(?P<option>\w+)$',views.yum_execute), 
    url(r'^tomcat/uploadfile',views.Uploadfile),
]
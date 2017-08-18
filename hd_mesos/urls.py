#!/usr/local/bin/python2.7
# encoding: utf-8

from django.conf.urls import url

import views


urlpatterns = [
    url(r'^$',views.Login),
    url(r'^login',views.Login),
    url(r'^index',views.index),
    url(r'^logout$',views.Logout),
    url(r'^userlist',views.UserList),
    url(r'^useradd',views.UserAdd),
    url(r'^pwdreset',views.PwdReset),
    url(r'^userdel',views.UserDel),
    url(r'^userlook',views.UserLook),
    url(r'^userinfo',views.UserInfo),
    url(r'^useredit',views.UserEdit),
    url(r'^usernamecheck',views.CheckUsername),
    url(r'^hostlist',views.HostList),
    url(r'^hostdel',views.host_del),
    url(r'^hostadd',views.host_add),
    url(r'^hostedit$',views.host_edit),
    url(r'^hostlook/(?P<hostip>[\d|.]+)/',views.host_look),
    url(r'^hostupdate$',views.host_update),
    url(r'^hostipcheck',views.CheckHostIP),
    url(r'^hostajaxget',views.HostAjaxGet),
    url(r'^grouptagajaxget',views.group_tag_ajaxget),
    url(r'^hostgroups',views.HostGroups),
    url(r'^groupadd',views.GroupAdd),
    url(r'^grouplook',views.GroupLook),
    url(r'^groupdel',views.GroupDel),
    url(r'^hostgrpcheck',views.CheckHostGrp),
    url(r'^privilegelist',views.PrivilegeList),
    url(r'^privilegelook',views.PrivilegeLook),
    url(r'^privilegedit',views.Privilegedit),
    url(r'^tasklist',views.task_list),
    url(r'^taskinfo/(?P<taskid>\d+)/',views.task_info),
    url(r'^taskack$',views.task_ack),
    url(r'^hostimp',views.host_import),
    url(r'^ticketstart',views.ticket_start),
    url(r'^taskchart',views.task_chart),
    url(r'^test/index',views.Test),
    url(r'^test/tables',views.Tables),
]
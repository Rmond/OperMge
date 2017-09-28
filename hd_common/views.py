# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from hd_mesos.models import HostInfo
from hd_mesos.views import login_check

@csrf_exempt
@login_check
def hostip_check(request):#添加主机前，判断主机是否存在
    if request.method == 'POST':
        HostIP = request.POST['HostIP']
        if HostInfo.objects.filter(ip=HostIP):
            return HttpResponse(0)
        else:
            return HttpResponse(1)


@csrf_exempt
@login_check
def hostidle_check(request):
    if request.method == 'POST':
        hostip = request.POST['HostIP']
        hostinfo = HostInfo.objects.get(ip=hostip)
        if hostinfo.idle:
            return HttpResponse(1)
        else:
            return HttpResponse(0)
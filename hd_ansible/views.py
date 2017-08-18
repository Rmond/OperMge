# -*- coding:utf-8 -*-
import json, os, time, datetime

from django.http.response import HttpResponse
from django.shortcuts import render , redirect
from django.views.decorators.csrf import csrf_exempt
from hd_mesos.views import login_check, user_role
from hd_mesos.models import HostInfo, HostGroup, Host_Group, User_Task
from models import MysqlAduit, OptionLog, SidInfo, Hostip_Port
from django.contrib.auth.hashers import make_password
from tasks import sid_init,yum_opt

# Create your views here.

ProNameitems = [{"Id":"oms", "Name":"OMS"}, {"Id":"wms", "Name":"WMS"}, {"Id":"scm", "Name":"SCM"}]
ProAppitems = [{"Id":"scm-web", "Name":"SCM-WEB", "Type":"scm"}, {"Id":"oms-web", "Name":"OMS-WEB", "Type":"oms"}]
ProVersionitems = [{"Id":"scm-web-1704", "Name":"SCM-WEB-1704", "Type":"scm-web"}, {"Id":"web", "Name":"WEB", "Type":"oms-web"}]


@login_check
def InventoryMge(request):
    with open("D:\hosts") as f:
        hosts = f.read().splitlines()
        for i in hosts:
            print i
    return render(request, "mesos/ansible/inventory/inventorymge.html", {"hosts":hosts})

@login_check
def PriList(request):
    prilist = MysqlAduit.objects.all()
    return render(request, "mesos/ansible/mysql/prilist.html", {"prilist":prilist})

@login_check
@user_role
def RollBack(request, tempath):
    tempath = tempath
    if request.method == 'POST':  # 返回执行结果
        hosts = request.POST.getlist('host_assets')
        groupids = request.POST.getlist('grp_assets')
        if len(hosts) + len(groupids) > 0:
            destserver = ""
            for host in hosts:
                destserver += host + ":"
            for groupid in groupids:
                group = HostGroup.objects.get(id=groupid)
                destserver += group.groupname.lower() + ":"
            war_srcpath = "/opt/war_manage/" + request.POST["ProName"] + "/" + request.POST["ProApp"] + "/" + request.POST["ProVersion"] + "/"
            war_destpath = request.POST["HostPath"]
            return render(request, tempath + "ansible/tomcat/rollbackres.html", {"hosts":destserver, "war_srcpath":war_srcpath, "war_destpath":war_destpath})
        else:
            return render(request, tempath + "ansible/tomcat/rollback.html", {"error":"请至少选择一个目标主机或主机组"})
    return render(request, tempath + "ansible/tomcat/rollback.html")  # 返回回滚界面

@login_check
@user_role
def ProjectDev(request, tempath):
    tempath = tempath
    return render(request, tempath + "ansible/tomcat/projectdev.html")

@csrf_exempt
@login_check
def Uploadfile(request):
    if request.method == 'POST':
        f = request.FILES.get('tomcat_war')
        print f.name
        return HttpResponse("上传完成")
    return render(request, "mesos/ansible/tomcat/projectdev.html")

@csrf_exempt
@login_check
def GroupHostGet(request):
    hostiplist = {}
    groupnamelist = {}
    hosts = HostInfo.objects.filter(user_host__username_id=request.session.get('username'))
    groups = HostGroup.objects.filter(user_hostgroup__username_id=request.session.get('username'))
    for host in hosts:
        hostiplist[host.ip] = host.ip
    for group in groups:
        groupnamelist[group.id] = group.groupname
    return HttpResponse(json.dumps({"groups":groupnamelist, "hosts":hostiplist}))
        
@csrf_exempt
@login_check
def yum_manage(request,option):
    hostlist = HostInfo.objects.all()
    grouplist = HostGroup.objects.all()
    if option == "install":
        temp_path="install.html"
    elif option == "update":
        temp_path="update.html"
    elif option == "delete":
        temp_path="delete.html"
    return render(request,"mesos/ansible/yum/"+temp_path ,{"hostlist":hostlist,"grouplist":grouplist})

@csrf_exempt
@login_check
def yum_execute(request,option):
    if request.method == 'POST':
        if option=="install":
            state="present"
        elif option=="update":
            state="latest"
        elif option=="delete":
            state="absent"
        hosts = request.POST.getlist('host_assets')
        groupids = request.POST.getlist('grp_assets')
        for i in groupids:
            for host_group in Host_Group.objects.filter(group_id=i):
                hosts.append(host_group.ip_id)
        hosts = list(set(hosts))
        hoststr = ":".join(hosts)
        extra_vars = {}
        extra_vars["hosts"] = hoststr
        extra_vars["softname"] = request.POST["Softname"]
        extra_vars["state"] = state
        startime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        username = request.session.get("username",None)
        #taskobj = yum_opt.apply_async([extra_vars])
        #user_task = User_Task(username_id = username,star_time = startime,taskid=taskobj.id,hosts=request.POST["Mhostip"]+":"+request.POST["Shostip"],taskname="yum_install")
        #user_task.save()
        return redirect('/hd_mesos/tasklist.html')
    
@csrf_exempt
@login_check
def MultiSelect(request):  
    if request.method == 'POST':
        received_data = json.loads(request.body)
        if received_data["MyColums"] == 'ProName':
            data = ProNameitems
        elif received_data["MyColums"] == 'ProApp':
            data = []
            for item in ProAppitems:
                if item["Type"] == received_data["parentId"]:
                    data.append(item)
        else:
            data = []
            for item in ProVersionitems:
                if item["Type"] == received_data["parentId"]:
                    data.append(item)
    return HttpResponse(json.dumps(data), content_type='application/json')

def AnsibleHandle(ymlfile, jsondata):
    shellstr = "ansible-playbook " + ymlfile + " --extra-vars '" + json.dumps(jsondata) + "'"
    return os.popen(shellstr).read().splitlines()


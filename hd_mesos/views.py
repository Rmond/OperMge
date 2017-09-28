# -*- coding:utf-8 -*-
import json,os,datetime
import xlrd

from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from models import HostInfo, Users,HostGroup,Host_Group,User_Host,User_Hostgroup,User_Task
from hd_ansible.models import Software
from django_celery_results.models import TaskResult
from celery.result import AsyncResult
from task_res_format import install_soft_res,mysql_sid_initres
from django.http.response import JsonResponse

def login_check(func):#登录检查装饰器
    def wrapper(request,*args,**kwargs):
        nickname = request.session.get('is_login',None)
        if not nickname:
            return redirect('/hd_mesos/login')
        return func(request,*args,**kwargs)
    return wrapper

def user_role(func):#用户角色检查装饰器
    def wrapper(request,*args,**kwargs):
        role = request.session.get('role',None)
        tempath = ""
        if role == 0:#管理员
            tempath="mesos/"
        elif role == 1:#普通用户
            tempath="mesos/custom/"
        return func(request,tempath)
    return wrapper
             
# Create your views here.
@csrf_exempt
def Login(request):
    if request.method == 'POST':
        Username = request.POST['username']
        Password = request.POST['password']
        try:
            user = Users.objects.get(username=Username)
            if check_password(Password,user.password):#登录判断
                request.session['is_login'] = user.nickname
                request.session['username'] = user.username
                request.session['role'] = user.role
                return redirect('/hd_mesos/index')
            else:#判断密码是否正确
                return render(request,"mesos/login.html",{'msg':'用户名或密码错误'})
        except Users.DoesNotExist:#判断用户是否存在
            return render(request,"mesos/login.html",{'msg':'用户名或密码错误'})         
    return render(request,"mesos/login.html")

@login_check
@user_role
def index(request,tempath):
    tempath = tempath
    user_count = Users.objects.count()
    host_count = HostInfo.objects.count()
    return render(request,tempath+"index.html",{"user_count":user_count,"host_count":host_count})

@csrf_exempt
@login_check 
def task_chart(request):
    name=[]
    num=[]
    for i in range(6,-1,-1):
        star_date=datetime.date.today()+datetime.timedelta(days=-i)
        stop_date=datetime.date.today()+datetime.timedelta(days=-i+1)
        user_task_ct = User_Task.objects.filter(star_time__gte = star_date).filter(star_time__lt = stop_date).count()
        name.append(star_date.strftime('%Y-%m-%d'))
        num.append(user_task_ct)
    return HttpResponse(json.dumps({"name":name,"num":num}))

@login_check 
def Logout(request):       
    del request.session['is_login']
    return redirect('/hd_mesos/login')

@login_check 
def user_list(request):#用户列表展示
    results = Users.objects.all()
    return render(request,"mesos/userlist.html",{'users':results})

@csrf_exempt
@login_check
def PwdReset(request):#密码重置为6个1
    if request.method == 'POST':
        Username = request.POST['Username']
        user = Users.objects.get(username=Username)
        user.password = make_password('111111')
        user.save()
        return HttpResponse("密码重置成功！")
        
@csrf_exempt
@login_check 
def UserAdd(request):#用户添加或修改
    if request.method == 'POST':
        Username = request.POST['Username']
        Nickname = request.POST['Nickname']
        Role = request.POST['Role']
        if Users.objects.filter(username=Username):#判断用户是否存在
            user = Users.objects.get(username=Username)
            user.nickname = Nickname
            user.role = Role
        else:
            Password = make_password('111111')
            user =  Users(username=Username,nickname=Nickname,password=Password,role=Role)
        user.save()
        return redirect('userlist.html')

@csrf_exempt
@login_check 
def UserDel(request):#用户删除
    if request.method == 'POST':
        Username = request.POST['Username']
        Users.objects.filter(username=Username).delete()
        return HttpResponse()
    
@csrf_exempt
@login_check 
def UserLook(request):#用户信息查看
    if request.method == 'POST':
        Username = request.POST['Username']
        user = Users.objects.get(username=Username)
        return HttpResponse(json.dumps({"username":user.username,"nickname":user.nickname,"role":user.role}))
    
@csrf_exempt
@login_check
def CheckUsername(request):#添加用户时，表单查询用户是否存在
    if request.method == 'POST':
        Username = request.POST['Username']
        if Users.objects.filter(username=Username):
            return HttpResponse(0)
        else:
            return HttpResponse(1)

@csrf_exempt
@login_check  
def UserInfo(request):
    if request.method == 'POST':
        Username = request.session.get('username',None)
        user = Users.objects.get(username = Username)
        return HttpResponse(json.dumps({'username':user.username,'nickname':user.nickname}))
    
@csrf_exempt
@login_check
def UserEdit(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        Nickname = request.POST['Nickname']
        Password = request.POST['Password']
        user = Users.objects.get(username = Username)
        user.nickname = Nickname
        user.password = make_password(Password)
        user.save()
        return HttpResponse()

@login_check
@user_role
def HostList(request,tempath):#主机列表
    tempath = tempath
    if "custom" in tempath:
        hosts = HostInfo.objects.filter(user_host__username_id = request.session.get('username'))
    else:
        hosts = HostInfo.objects.all()
    results = {'hosts':hosts}
    return render(request,tempath+"hostlist.html",results)

@login_check
@user_role
def HostGroups(request,tempath):#主机组列表
    tempath = tempath
    if "custom" in tempath:
        groups = HostGroup.objects.filter(user_hostgroup__username_id = request.session.get('username'))
    else:
        groups = HostGroup.objects.all()
    results = {'groups':groups}
    return render(request,tempath+"hostgroups.html",results)

@csrf_exempt
@login_check
def host_del(request):#主机删除
    if request.method == 'POST':
        HostIP = request.POST['HostIP']
        HostInfo.objects.filter(ip=HostIP).delete()
        return HttpResponse()

@csrf_exempt
@login_check
def host_add(request):#主机添加或修改
    if request.method == 'POST':
        HostIP = request.POST['HostIP']
        HostName = request.POST['HostName']
        SelectTags = request.POST.getlist('tags_select')
        SelectGroupId = request.POST.getlist('asset_select')
        tags = ""
        for tagid in SelectTags:
            tags+=Software.objects.get(id=tagid).softname+" "  
        hostinfo =  HostInfo(hostname=HostName,ip=HostIP,tags=tags)
        hostinfo.save()
        for i in SelectGroupId:#判断主机组是否被选中
            host_group = Host_Group(group_id=i,ip_id=HostIP)
            host_group.save()
        return redirect('hostlist.html')

@csrf_exempt
@login_check
def host_look(request,hostip):#主机信息更改
    groupsel = {}
    groupunsel = {}
    tagsel = {}
    tagunsel = {}
    hostinfo=HostInfo.objects.get(ip=hostip)
    for group in HostGroup.objects.all():#循环主机组
        try:#判断主机组是否包含此主机
            Host_Group.objects.get(ip_id=hostip,group_id=group.id)
            groupsel[group.id]=group.groupname
        except Host_Group.DoesNotExist:
            groupunsel[group.id]=group.groupname
    for tagobj in Software.objects.all():
        if tagobj.softname in hostinfo.tags:
            tagsel[tagobj.id] = tagobj.softname
        else:
            tagunsel[tagobj.id] = tagobj.softname
    return render(request,"mesos/hostedit.html",{"hostinfo":hostinfo,"groupsel":groupsel,"groupunsel":groupunsel,"tagsel":tagsel,"tagunsel":tagunsel,"vginfo_list":json.loads(hostinfo.vginfo)})

@csrf_exempt
@login_check
def host_edit(request):
    if request.method == 'POST':
        HostIP = request.POST['HostIP']
        SelectTags = request.POST.getlist('tags_select')
        SelectGroupId = request.POST.getlist('asset_select')
        UnselectGroupId = request.POST.getlist('assets')
        hostinfo = HostInfo.objects.get(ip=HostIP)
        hostinfo.hostname= request.POST['HostName']
        tagstr = ""
        for tag in SelectTags:
            tagstr+=Software.objects.get(id=tag).softname+" "
        hostinfo.tags=tagstr
        hostinfo.save()
        for i in SelectGroupId:#判断主机组是否被选中
            try:
                host_group = Host_Group.objects.get(group_id=i,ip_id=HostIP)
            except Host_Group.DoesNotExist:
                host_group = Host_Group(group_id=i,ip_id=HostIP)
                host_group.save()
        for j in UnselectGroupId:
            host_group = Host_Group.objects.filter(group_id=j,ip_id=HostIP).delete()
        return redirect('hostlist.html')

@csrf_exempt
@login_check    
def host_update(request):
    if request.method == 'POST':
        checklist=request.POST.getlist('checklist')
        if "checkall" in checklist:
            host="all"
        else:
            host=":".join(checklist)

        return HttpResponse()

@csrf_exempt
@login_check
def HostDetailInfo(request):#主机详细信息展示
    if request.method == 'POST':
        HostIP = request.POST['HostIP']
        hostinfo = HostInfo.objects.get(ip=HostIP)
    return render(request,{'hostinfo':hostinfo})

@login_check
def GroupAdd(request):
    if request.method == 'POST':
        Groupname = request.POST['Groupname']
        Groupid = request.POST['Groupid']
        if Groupid: #判断主机组是否存在，如果存在更改相应的主机名，不存在添加主机组
            hostgroup=HostGroup.objects.get(id=Groupid)
            hostgroup.groupname = Groupname
        else:
            hostgroup = HostGroup(groupname=Groupname)
        hostgroup.save()
        SelectGroupId = request.POST.getlist('asset_select')#属于主机组的主机
        UnSelectGroupId = request.POST.getlist('assets')#不属于主机组的主机
        for i in SelectGroupId:
            try:
                Host_Group.objects.get(ip_id=i,group_id=hostgroup.id)#判断主机是否添加过，添加过则不操作
            except Host_Group.DoesNotExist:
                host_group = Host_Group(ip_id=i,group_id=hostgroup.id)#把主机添加到跟主机组的关系表
                host_group.save()
        for j in UnSelectGroupId:
            Host_Group.objects.filter(ip_id=j,group_id=hostgroup.id).delete()#删除在非选中框中的主机
        return redirect('hostgroups.html')

@csrf_exempt
@login_check
def GroupLook(request):
    if request.method == 'POST':
        selected = {}
        unselected = {}
        Groupname = request.POST['Groupname']
        hostgroup=HostGroup.objects.get(groupname=Groupname)
        for host in HostInfo.objects.all():#循环判断主机是否属于主机组
            try:
                Host_Group.objects.get(ip_id=host.ip,group_id=hostgroup.id)
                selected[host.ip]=host.ip
            except Host_Group.DoesNotExist:
                unselected[host.ip]=host.ip
        return HttpResponse(json.dumps({"groupid":hostgroup.id,"groupname":hostgroup.groupname,"selected":selected,"unselected":unselected}))

@csrf_exempt
@login_check
def CheckHostGrp(request):
    if request.method == 'POST':
        HostGrp = request.POST['HostGrp']
        if HostGroup.objects.filter(groupname=HostGrp):
            return HttpResponse(0)
        else:
            return HttpResponse(1)
        
@csrf_exempt
@login_check
def GroupDel(request):
    if request.method == 'POST':
        Groupname = request.POST['Groupname']
        HostGroup.objects.filter(groupname=Groupname).delete()
        return HttpResponse()

       
@csrf_exempt
@login_check
def group_tag_ajaxget(request):
    groups = HostGroup.objects.all()
    tags = Software.objects.all()
    grouplist = {}
    taglist = {}
    for group in groups:
        grouplist[group.id] = group.groupname
    for tag in tags:
        taglist[tag.id] = tag.softname
    return HttpResponse(json.dumps({"grouplist":grouplist,"taglist":taglist}))

@csrf_exempt
@login_check
def HostAjaxGet(request):
    hosts = HostInfo.objects.all()
    hostlist = {}
    for host in hosts:
        hostlist[host.ip]=(host.ip)
    return HttpResponse(json.dumps({"hostlist":hostlist}))

@csrf_exempt
@login_check
def PrivilegeList(request):
    users = Users.objects.all()
    return render(request,"mesos/privilegelist.html",{'users':users})

@csrf_exempt
@login_check
def PrivilegeLook(request):
    if request.method == 'POST':
        grpselected = {}
        grpunselected = {}
        hostselected = {}
        hostunselected = {}
        Username= request.POST['Username']
        for host in HostInfo.objects.all():#循环判断主机是否被授权
            try:
                User_Host.objects.get(username_id=Username,ip_id=host.ip)
                hostselected[host.ip] = host.ip
            except User_Host.DoesNotExist:
                hostunselected[host.ip] = host.ip
        for group in HostGroup.objects.all():#循环判断主机组是否被授权
            try:
                User_Hostgroup.objects.get(username_id=Username,group_id=group.id)
                grpselected[group.id] = group.groupname
            except User_Hostgroup.DoesNotExist:
                grpunselected[group.id] = group.groupname
    return HttpResponse(json.dumps({"username":Username,"hostselected":hostselected,"hostunselected":hostunselected,"grpselected":grpselected,"grpunselected":grpunselected}))

@csrf_exempt
@login_check
def Privilegedit(request):
    if request.method == 'POST':
        Username = request.POST['Username']
        SelectGroupId = request.POST.getlist('grp_asset_select')
        UnSelectGroupId = request.POST.getlist('grp_assets')
        SelectHost = request.POST.getlist('host_asset_select')
        UnSelectHost = request.POST.getlist('host_assets')
        for i in SelectGroupId:
            try:
                User_Hostgroup.objects.get(username_id=Username,group_id=i)#判断主机组是否添加过，添加过则不操作
            except User_Hostgroup.DoesNotExist:
                user_hostgroup = User_Hostgroup(username_id=Username,group_id=i)#把主机组添加到跟用户的关系表
                user_hostgroup.save()
        for j in UnSelectGroupId:
            User_Hostgroup.objects.filter(username_id=Username,group_id=j).delete()
        for x in SelectHost:
            try:
                User_Host.objects.get(username_id=Username,ip_id=x)
            except User_Host.DoesNotExist:
                user_host = User_Host(username_id = Username,ip_id = x)
                user_host.save()
        for y in UnSelectHost:
            User_Host.objects.filter(username_id = Username,ip_id = y).delete()
    return redirect('privilegelist.html')

@login_check
def task_list(request):
    tasklist = User_Task.objects.filter(username_id=request.session.get('username',None))
    for task in tasklist:
        if not task.result:
            task.status = AsyncResult(task.taskid).state
            try:
                taskres = TaskResult.objects.get(task_id=task.taskid)
                task.date_done = taskres.date_done
                result = json.loads(taskres.result)
                task.result = json.dumps(result["ansible_res"])
                task.status = result["status"]
            except TaskResult.DoesNotExist:
                pass
            task.save()
    return render(request,"mesos/tasklist.html",{"tasklist":tasklist})

@login_check
def task_info(request,*args,**kwargs):
    user_task = User_Task.objects.get(id = kwargs['taskid'])
    result = user_task.result.replace("[","").replace("]","").replace("\"","").split(",")
    return render(request,"mesos/taskinfo.html",{"user_task":user_task,"result":result})

@csrf_exempt
@login_check
def task_ack(request):
    if request.method == 'POST':
        usertaskid = request.POST['id']
        user_task = User_Task.objects.get(id=usertaskid)
        user_task.acked = True
        user_task.save()
        return HttpResponse()

@csrf_exempt
@login_check
def host_import(request):
    if request.method == "POST":
        f = request.FILES.get('xlsname')
        filename = os.path.join("D:\\",f.name)
        with open(filename,'wb') as fobj:
            for chunck in f.chunks():
                fobj.write(chunck)
        xlsfile = xlrd.open_workbook(filename)
        xlstable = xlsfile.sheet_by_index(0)
        rowscount = xlstable.nrows
        for num in range(1,rowscount):
            hostname = xlstable.row_values(num)[0]
            hostip = xlstable.row_values(num)[1]
            try:
                hostinfo = HostInfo.objects.get(ip=hostip)
                hostinfo.hostname = hostname
            except HostInfo.DoesNotExist:
                hostinfo = HostInfo(hostname=hostname,ip=hostip)
            hostinfo.save()
        return redirect('hostlist.html')

def ticket_start(request):
    return render(request,"mesos/ticketstart.html")

from rest_framework import serializers
# Serializers define the API representation.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Users
        fields = ('username', 'nickname', 'password', 'role')

@csrf_exempt               
def Test(request):
    #result = Test123.objects.get(id=1).result
    #return HttpResponse(json.loads(result)["status"])
    users = Users.objects.all()
    serializer = UserSerializer(users,many=True)
    return JsonResponse(serializer.data,safe=False)

from django_celery_beat.models import PeriodicTask
def Tables(request):
    
    return HttpResponse()
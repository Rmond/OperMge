# -*- coding:utf-8 -*-
import os,json
from celery import shared_task
from hd_mesos.models import HostInfo
from models import Hostip_Port,SidInfo

@shared_task
def up(f):
    filename = os.path.join("/tmp/",f.name)
    with open(filename,'wb') as fobj:
        for chunck in f.chunks():
            fobj.write(chunck)
    return "OK"

@shared_task
def upload(f):
    filename = os.path.join("/tmp/",f.name)
    with open(filename,'wb') as fobj:
        for chunck in f.chunks():
            fobj.write(chunck)
    return "OK"

@shared_task
def install(extra_vars,softinfo):
    result = {}
    status = "SUCCESS"
    try:
        ansible_res = ansiblehandle("/opt/ansible/roles/site.yml",extra_vars)
        for hostip in extra_vars["hosts"].split(":"):#循环读取执行主机
            birefres = filter(lambda x:hostip in x,ansible_res)[-1]
            if hostip in birefres and "failed=0" in birefres:
                hostinfo = HostInfo.objects.get(ip=hostip)
                if not hostinfo.software:
                    hostinfo.software += softinfo
                else:
                    hostinfo.software += ","+softinfo
                hostinfo.save()
                if "mysql" in softinfo:
                    hostip_port = Hostip_Port(hostip = hostip)
                    hostip_port.save()
            else:
                status = "FAILED"
    except Exception:
        status = "FAILED"
    finally:
        hostinfo2 = HostInfo.objects.get(ip=hostip)
        hostinfo2.idle = True
        hostinfo2.save()
    result["ansible_res"] = ansible_res
    result["status"] = status
    return result

@shared_task
def update(extra_vars,softinfo):
    result = {}
    status = "SUCCESS"
    try:
        ansible_res = ansiblehandle("/opt/ansible/roles/site.yml",extra_vars)
        for hostip in extra_vars["hosts"].split(":"):#循环读取执行主机
            birefres = filter(lambda x:hostip in x,ansible_res)[-1]
            if hostip in birefres and "failed=0" in birefres:
                hostinfo = HostInfo.objects.get(ip=hostip)
                if not hostinfo.software:
                    hostinfo.software += softinfo
                else:
                    hostinfo.software += ","+softinfo
                hostinfo.save()
            else:
                status = "FAILED"
    except Exception:
        status = "FAILED"
    finally:
        hostinfo2 = HostInfo.objects.get(ip=hostip)
        hostinfo2.idle = True
        hostinfo2.save()
    result["ansible_res"] = ansible_res
    result["status"] = status
    return result

@shared_task()
def sid_init(mextra_vars,sextra_vars):
    result = {}
    reslist = []
    try:
        res1 = ansiblehandle("/opt/ansible/roles/site.yml",mextra_vars)
        reslist.append(res1)
        res2 = ansiblehandle("/opt/ansible/roles/site.yml",sextra_vars)
        reslist.append(res2)
        if reslist.count("failed=0") == 2:
            master_sid_info = SidInfo()
            master_sid_info.sidname = mextra_vars["sid"]
            master_sid_info.hostip=mextra_vars["hosts"]
            master_sid_info.port=mextra_vars["port"]
            master_sid_info.socketpath="/mysql_data/"+master_sid_info.sidname+"/tmp/mysql.sock"
            master_sid_info.password=mextra_vars["password"]
            master_sid_info.replpassword=mextra_vars["replpassword"]
            master_sid_info.data_size=mextra_vars["data_size"]
            master_sid_info.save()
            slave_sid_info = SidInfo()
            slave_sid_info.sidname = sextra_vars["sid"]
            slave_sid_info.hostip=sextra_vars["hosts"]
            slave_sid_info.port=sextra_vars["port"]
            slave_sid_info.socketpath="/mysql_data/"+slave_sid_info.sidname+"/tmp/mysql.sock"
            slave_sid_info.password=sextra_vars["password"]
            slave_sid_info.replpassword=sextra_vars["replpassword"]
            slave_sid_info.data_size=sextra_vars["data_size"]
            slave_sid_info.save()
            hostip_port=Hostip_Port.objects.get(hostip=mextra_vars["hosts"])
            hostip_port.port=hostip_port.port+1
            hostip_port2=Hostip_Port.objects.get(hostip=sextra_vars["hosts"])
            hostip_port2.port=hostip_port2.port+1
            status = "SUCCESS"
        else:
            status = "FAILED"
    except Exception:
        status = "FAILED"
    finally:
        hostinfo = HostInfo.objects.get(ip=mextra_vars["hosts"])
        hostinfo.idle = True
        hostinfo.save()
        hostinfo2 = HostInfo.objects.get(ip=mextra_vars["hosts"])
        hostinfo2.idle = True
        hostinfo2.save()
    result["ansible_res"] = reslist
    result["status"] = status
    return result

@shared_task()
def yum_opt(extra_vars):
    result = {}
    status = "SUCCESS"
    try:
        ansible_res = ansiblehandle("/opt/ansible/yum/install.yml",extra_vars)
        for hostip in extra_vars["hosts"].split(":"):#循环读取执行主机
            birefres = filter(lambda x:hostip in x,ansible_res)[-1]
            if hostip in birefres and "failed=0" not in birefres:
                status = "FAILED"
    except Exception:
        status = "FAILED"
    result["ansible_res"] = ansible_res
    result["status"] = status
    return result

@shared_task()
def db_dump(extra_vars,flag=""):
    result = {}
    status = "SUCCESS"
    try:
        ansible_res = ansiblehandle("/opt/ansible/mysql/database_exp.yml",extra_vars)
        if "failed=0" not in ansible_res[-2]:
            status = "FAILED"
    except Exception:
        status = "FAILED"
    result["ansible_res"] = ansible_res
    result["status"] = status
    return result

def ansiblehandle(ymlfile,jsondata):
    shellstr = "ansible-playbook "+ymlfile+" --extra-vars '"+json.dumps(jsondata)+"'"
    return os.popen(shellstr).read().splitlines()

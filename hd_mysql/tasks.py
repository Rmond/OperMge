# -*- coding:utf-8 -*-
import os,json
from celery import shared_task
from hd_mesos.models import HostInfo
from hd_ansible.models import Hostip_Port,SidInfo

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
def sid_update_task(mextra_vars,sextra_vars):
    result = {}
    reslist = []
    res1 = ansiblehandle("/opt/ansible/roles/site.yml",mextra_vars)
    reslist.append(res1)
    res2 = ansiblehandle("/opt/ansible/roles/site.yml",sextra_vars)
    reslist.append(res2)
    if filter(lambda x:"failed=0" in x,res1) and filter(lambda x:"failed=0" in x,res2):
        master_sid_info = SidInfo.objects.get(sidname=mextra_vars["sid"])
        mhostinfo = HostInfo.objects.get(ip=mextra_vars["hosts"])
        mhostinfo.memory_used = mhostinfo.memory_used+(int(master_sid_info.buffer_pool)-int(mextra_vars["buffer_pool"]))*1024
        mhostinfo.memory_free = mhostinfo.memory_total - mhostinfo.memory_used
        mhostinfo.save()
        master_sid_info.data_size=mextra_vars["data_size"]
        master_sid_info.buffer_pool=mextra_vars["buffer_pool"]
        master_sid_info.save()
        slave_sid_info = SidInfo.objects.get(sidname=sextra_vars["sid"])
        shostinfo = HostInfo.objects.get(ip=sextra_vars["hosts"])
        shostinfo.memory_used = shostinfo.memory_used+(int(slave_sid_info.buffer_pool)-int(sextra_vars["buffer_pool"]))*1024
        shostinfo.memory_free = shostinfo.memory_total - shostinfo.memory_used
        shostinfo.save()
        slave_sid_info.data_size=sextra_vars["data_size"]
        slave_sid_info.buffer_pool=sextra_vars["buffer_pool"]
        slave_sid_info.save()
        update_info(mextra_vars["hosts"]+":"+sextra_vars["hosts"])
        status = "SUCCESS"
    else:
        status = "FAILED"
    hostinfo = HostInfo.objects.get(ip=mextra_vars["hosts"])
    hostinfo.idle = True
    hostinfo.save()
    hostinfo2 = HostInfo.objects.get(ip=sextra_vars["hosts"])
    hostinfo2.idle = True
    hostinfo2.save()
    result["ansible_res"] = reslist
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

# -*- coding:utf-8 -*-
import os,json
from celery import shared_task
from models import HostInfo

@shared_task
def get_info(f):
    
    return

def ansiblehandle(host):
    shellstr = "ansible "+host+" -m setup"
    return os.popen(shellstr).read().splitlines()

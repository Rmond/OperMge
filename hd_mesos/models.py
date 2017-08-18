from __future__ import unicode_literals

from django.db import models

# Create your models here.
class HostInfo(models.Model):
    hostname=models.CharField(max_length=32)
    ip=models.CharField(max_length=16,primary_key=True)
    software = models.CharField(max_length=128,default="")
    tags = models.CharField(max_length=64,default="")
    idle = models.BooleanField(default=True)
    vginfo = models.TextField(null=True)
    memory_total = models.IntegerField(default=0)
    memory_used = models.IntegerField(default=0)
    memory_free = models.IntegerField(default=0)

class Users(models.Model):
    username = models.CharField(max_length=32,primary_key=True)
    nickname = models.CharField(max_length=16)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(default=1)

class HostGroup(models.Model):
    id = models.AutoField(primary_key=True)
    groupname = models.CharField(max_length=32,unique=True)
    
class Host_Group(models.Model):
    id = models.AutoField(primary_key=True)
    ip = models.ForeignKey(HostInfo)
    group = models.ForeignKey(HostGroup)
    
class User_Host(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(Users)
    ip = models.ForeignKey(HostInfo)

class User_Hostgroup(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(Users)
    group = models.ForeignKey(HostGroup)
    
class User_Task(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.ForeignKey(Users)
    taskid = models.CharField(max_length=48,default="")
    taskname = models.CharField(max_length=32,default="")
    acked = models.BooleanField(default=False)
    star_time=models.DateTimeField()
    hosts=models.CharField(max_length=128)
    status=models.CharField(max_length=50,default="Running")
    result=models.TextField(null=True)
    date_done=models.DateTimeField(null=True)
    

"""Handu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
#from django.contrib import admin
from rest_framework import routers
from hd_demo import views
#router = routers.DefaultRouter()
#router.register(r'users', views.user_list)

urlpatterns = [
    url(r'^api/', include('hd_demo.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-auth/login',views.LoginViewSet.as_view()),
    url(r'^hd_mesos/', include('hd_mesos.urls',namespace="hd_mesos")),
    url(r'^hd_ansible/', include('hd_ansible.urls',namespace="hd_ansible")),
    url(r'^hd_mysql/', include('hd_mysql.urls',namespace="hd_mysql")),
    url(r'^hd_common/', include('hd_common.urls',namespace="hd_common")),
]

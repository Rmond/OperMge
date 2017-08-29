# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from hd_mesos.models import Users
from rest_framework import viewsets
from serializers import UserSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.contrib.auth.hashers import make_password

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited..
#     """
#     queryset = Users.objects.all()
#     serializer_class = UserSerializer

@csrf_exempt
@api_view(['GET','POST'])
def user_list(request,format=None):#用户列表展示
    if request.method == 'GET':
        users = Users.objects.all()
#         serializer_context = {
#        'request': Request(request),
#             }
        serializer = UserSerializer(users,many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        request.data["password"] = make_password(request.data["password"])
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def user_detail(request,username,format=None):#用户详细信息展示
    """
    Retrieve, update or delete a snippet instance.
    """
    try:
        user = Users.objects.get(username=username)
    except Users.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == 'PUT':
        request.data["password"] = make_password(request.data["password"])
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
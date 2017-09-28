# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from auth import CustomAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from hd_mesos.models import Users
from serializers import UserSerializer


class LoginViewSet(APIView):
    """
    API endpoint that allows users to be viewed or edited..
    """
    users = Users.objects.all()
    serializer_class = UserSerializer
    
    def post(self, request):
        try:
            username = request.data.get('username')
            password = request.data.get('password')
            user = Users.objects.get(username=username)
            if check_password(user.password,password):
                print user
                serializer = UserSerializer({'id': user.id, 'username': user.username})
                return Response(serializer.data)
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        except Users.DoesNotExist:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

@csrf_exempt
@api_view(['GET','POST'])
@authentication_classes((SessionAuthentication, CustomAuthentication))
@permission_classes((IsAuthenticated,))
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
@authentication_classes((SessionAuthentication, CustomAuthentication))
@permission_classes((IsAuthenticated,))
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
    
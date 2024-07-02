from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
from django.contrib.auth.models import User

from . import models
from . import serializers

from django.shortcuts import  get_object_or_404
#from django.contrib.auth.models import Group, User

from rest_framework.views import APIView
import requests
from rest_framework.permissions import AllowAny

class UserInfoView(generics.RetrieveUpdateAPIView): # single user view accessed by user and admin
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_object(self):
        # Get the username of the authenticated user
        username = self.request.user.username

        # Get the User object using the username
        user_id = get_object_or_404(User, username=username).id

        return get_object_or_404(models.UserInfo, user_id=user_id)
    def perform_update(self, serializer): #Update User Info
        user = self.request.user
        serializer.save(user=user)


class UserInfoCreateView(generics.CreateAPIView):#Create User Info
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def perform_create(self, serializer):
        user = self.request.user #Get The Username from the body
        serializer.save(user=user)
        
class AllUserInfoView(generics.ListAPIView): # all users view accessed by admin and users to create user info
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    # search_fields = ['id']
    ordering_fields = ['age', 'weight', 'height']
    
    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]
    


class HistoryRecordView(generics.ListCreateAPIView):
    queryset = models.HistoryRecord.objects.all()
    serializer_class = serializers.HistoryRecordSerializer
    
class SingleHistoryRecordView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.HistoryRecord.objects.all()
    serializer_class = serializers.HistoryRecordSerializer

# class UserActivationView(APIView):
#     def get (self, request, uid, token):
#         protocol = 'https://' if request.is_secure() else 'http://'
#         web_url = protocol + request.get_host()
#         post_url = web_url + "/auth/users/activate/"
#         post_data = {'uid': uid, 'token': token}
#         result = requests.post(post_url, data = post_data)
#         content = result.text
#         return Response(content)

class UserActivationView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = f"{web_url}/auth/users/activation/"
        post_data = {'uid': uid, 'token': token}
        
        try:
            result = requests.post(post_url, json=post_data)  # Sending JSON data
            result.raise_for_status()  # Raise an error for bad status codes
            content = result.json()  # Assuming the response is JSON
        except requests.exceptions.RequestException as e:
            content = {'error': str(e)}
        
        return Response(content)

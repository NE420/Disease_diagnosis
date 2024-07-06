from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.contrib.auth.models import User
from .serializers import ChatSessionSerializer, InteractionSerializer, ChatSessionInteractSerializer
from .models import ChatSession, Interaction
from . import models
from . import serializers
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import  get_object_or_404
#from django.contrib.auth.models import Group, User
from rest_framework.views import APIView
import requests
from djoser.serializers import PasswordResetConfirmSerializer

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
    
class PasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, uid, token):
        protocol = 'https://' if request.is_secure() else 'http://'
        web_url = protocol + request.get_host()
        post_url = f"{web_url}/auth/users/reset_password_confirm/"
        post_data = {
            'uid': uid,
            'token': token,
            'new_password': request.data.get('new_password')
        }
        
        try:
            result = requests.post(post_url, json=post_data)
            result.raise_for_status()  # Raise an error for bad status codes
            content = result.json()  # Assuming the response is JSON
        except requests.exceptions.RequestException as e:
            content = {'error': str(e)}
        
        return Response(content)

#History Views
#With Get Request Retrieves user previous Sessions and with post create a new session
class ChatSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = ChatSessionSerializer
    permission_classes = [IsAuthenticated,IsOwner]

    def get_queryset(self):
        user = self.request.user
        return ChatSession.objects.filter(user=user)

    def perform_create(self, serializer):
        user = self.request.user
        print(user)
        serializer.save(user=user)
#Uses retrieve api view to return session details for a specific session id for a specific user
class ChatSessionDetailView(generics.RetrieveAPIView):
    serializer_class = ChatSessionInteractSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ChatSession.objects.filter(user=self.request.user)
#Use Get to retrieve the messages of a specific interactions and use post to add a new interaction

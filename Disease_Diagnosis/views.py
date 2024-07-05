from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status
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
from rest_framework.permissions import AllowAny
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
    def post(self, request, uid, token):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
class InteractionListCreateView(generics.ListCreateAPIView):
    serializer_class = InteractionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        chat_session_id = self.request.query_params.get('chat_session')
        return Interaction.objects.filter(chat_session__id=chat_session_id, chat_session__user=self.request.user)

    def perform_create(self, serializer):
        chat_session = ChatSession.objects.get(id=self.request.data['chat_session'])
        if chat_session.user != self.request.user:
            raise PermissionDenied("You are not allowed to add interactions to this session.")
        serializer.save(chat_session=chat_session)
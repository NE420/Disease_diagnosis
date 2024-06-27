from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from .permissions import IsOwner
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import status

from . import models
from . import serializers

from django.shortcuts import  get_object_or_404
#from django.contrib.auth.models import Group, User

class UserInfoView(generics.RetrieveUpdateDestroyAPIView): # single user view accessed by user and admin
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer
    permission_classes = [IsAuthenticated, IsOwner]
     
    def get_object(self):
        user_id = self.kwargs.get('user_id')    # Retrieve the profile of the user specified by user_id
        return get_object_or_404(models.UserInfo, user_id=user_id)

class AllUserInfoView(generics.ListCreateAPIView): # all users view accessed by admin and users to create user info
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

class CurrentUserIdView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated] # could be changed to IsAdminUser to make it safer 

    def get(self, request, *args, **kwargs):
        return Response({'user_id': request.user.id})
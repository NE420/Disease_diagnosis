from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework import viewsets
from rest_framework import status

from . import models
from . import serializers

# from django.shortcuts import  get_object_or_404
from django.contrib.auth.models import Group, User

class UserInfoView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.UserInfoSerializer

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.request.method != 'GET':
    #         permission_classes = [IsAuthenticated]

    #     return [permission() for permission in permission_classes]

class AllUserInfoView(generics.ListCreateAPIView):
    queryset = models.UserInfo.objects.all()
    serializer_class = serializers.ALLUserInfoSerializer
    # search_fields = ['id']
    ordering_fields = ['age', 'weight', 'height']

    # def get_permissions(self):
    #     permission_classes = []
    #     if self.request.method != 'GET':
    #         permission_classes = [IsAuthenticated]

    #     return [permission() for permission in permission_classes]

class HistoryRecordView(generics.ListCreateAPIView):
    queryset = models.HistoryRecord.objects.all()
    serializer_class = serializers.HistoryRecordSerializer
    
class singleHistoryRecordView(generics.RetrieveUpdateDestroyAPIView):
    queryset = models.HistoryRecord.objects.all()
    serializer_class = serializers.HistoryRecordSerializer
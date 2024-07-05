from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal
from . import models
from djoser.serializers import ActivationSerializer
from django.contrib.auth import get_user_model

from .models import ChatSession, Interaction


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserInfoSerializer(serializers.ModelSerializer):
    BMI = serializers.SerializerMethodField(method_name='CalcBMI', read_only=True)
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.UserInfo   
        fields = ['user', 'age', 'gender', 'weight', 'height', 'BMI','image']
        
    def CalcBMI(self, user:models.UserInfo):
        height_meter = user.height / 100
        bmi =  user.weight/(height_meter**2)
        if bmi <= 18.5:
            cat = "UnderWeight"
        elif 18.5 < bmi <= 24.9:
            cat = "HealthyWeight"
        elif 25.0 <= bmi <= 29.9:
            cat = "OverWeight"
        else:
            cat = "Obese"
        return cat
        

class CustomActivationSerializer(ActivationSerializer):
    def activate(self, *args, **kwargs):
        user = super().activate(*args, **kwargs)
        if user:
            user.is_active = True
            user.save()
        return user
class InteractionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'chat_session', 'user_question', 'model_answer', 'timestamp']
#exclude interactions
class ChatSessionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'title', 'started_at']

 #Retrieve a specific session detail with interactions
class ChatSessionInteractSerializer(serializers.ModelSerializer):
    interactions = InteractionSerializer(many=True, read_only=True)
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'title', 'started_at', 'interactions']

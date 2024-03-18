from rest_framework import serializers
from django.contrib.auth.models import User
from decimal import Decimal
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserInfoSerializer(serializers.ModelSerializer):
    BMI = serializers.SerializerMethodField(method_name='CalcBMI', read_only=True)
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=serializers.CurrentUserDefault()
    )
    class Meta:
        model = models.UserInfo   
        fields = ['user', 'age', 'gender', 'weight', 'height', 'BMI']
        
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
        
class HistoryRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.HistoryRecord
        fields = ['id','user','chat', 'feedback']
        
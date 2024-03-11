from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    age = models.SmallIntegerField(db_index=True)
    GENDER_CHOICE = {
        "F": "Female",
        "M": "Male",
    }
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    weight = models.DecimalField(db_index=True, max_digits=5, decimal_places=2)
    height = models.DecimalField(db_index=True, max_digits=5, decimal_places=2)
    
#class UserHistory(models.Model):

#class DocSpecialty(models.Model):
    
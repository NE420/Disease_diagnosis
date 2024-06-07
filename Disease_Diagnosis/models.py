from django.db import models
from django.contrib.auth.models import User, Group
# Create your models here.

def upload_path(instance, filename): # returns image path
    return '/'.join(['images', str(instance.user.username), filename])

class UserInfo(models.Model): # accessed by user and admin
    user = models.OneToOneField(User, on_delete= models.CASCADE)
    age = models.SmallIntegerField(db_index=True)
    GENDER_CHOICE = {
        "F": "Female",
        "M": "Male",
    }
    gender = models.CharField(max_length=1, choices=GENDER_CHOICE)
    weight = models.DecimalField(db_index=True, max_digits=5, decimal_places=2)
    height = models.DecimalField(db_index=True, max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to=upload_path, null=True, blank=True)
    
class HistoryRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.CharField(max_length=950)
    feedback =  models.CharField(max_length=350, blank=True)
    
    
#class DocSpecialty(models.Model):
    
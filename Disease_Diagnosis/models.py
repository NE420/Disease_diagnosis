from django.db import models
from django.contrib.auth.models import User, Group
import os

import pyrebase

config = {

  "apiKey": "AIzaSyCIApd-0IFqzx0LUUp9cTRmdDPbT8mQECk",
  "authDomain": "diseasediagnosis-c0f74.firebaseapp.com",
  "projectId": "diseasediagnosis-c0f74",
  "databaseURL": "https://dummy-url.firebaseio.com",
  "storageBucket": "diseasediagnosis-c0f74.appspot.com",
  "messagingSenderId": "971295866182",
  "appId": "1:971295866182:web:c0cd0d8e2d55493ee1f947",
  "measurementId": "G-48JYS9EQGB"
}

firebase = pyrebase.initialize_app(config)
storage = firebase.storage()

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
    image = models.ImageField(upload_to=upload_path, blank=True,null= True)


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.image:
            filename = os.path.basename(self.image.name)
            storagePath= '/'.join(['images', str(self.user.username), filename])
            # print(storagePath)
            storage.child(storagePath).put(self.image.path)

        # if os.path.isfile(localpath):
        #os.remove(localpath)
        
    def __str__(self):
        return self.user.username
    

    
class HistoryRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    chat = models.CharField(max_length=950)
    feedback =  models.CharField(max_length=350, blank=True)
    
    
#class DocSpecialty(models.Model):
    
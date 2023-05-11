from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Course(models.Model):
    coursenumber = models.CharField(max_length=20)
    coursecode = models.CharField(max_length=50)
    instructorname = models.CharField(max_length=50)
    startdate = models.DateField()
    enddate = models.DateField()
    totalclasses = models.CharField(max_length=10)
    slots = models.CharField(max_length=50)
    def __str__(self):
        return self.coursenumber
    
class Times(models.Model):
    codes = models.CharField(max_length=100)
    codestime = models.CharField(max_length=100)
    codenumber = models.CharField(max_length=20)
    def __str__(self):
        return self.codenumber

class Attendancemodel(models.Model):
    username = models.CharField(max_length = 20)
    date = models.DateField()
    time = models.CharField(max_length=20)
    coursecode = models.CharField(max_length=20)
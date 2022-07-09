from statistics import mode
from django.db import models
from matplotlib.pyplot import cla

# Create your models here.

class Registration(models.Model):
    fullname = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    emails = models.EmailField(max_length=100)
    contacts = models.CharField(max_length=100)
    passwords = models.CharField(max_length=100) 
    gender = models.CharField(max_length=100)
    users = models.CharField(max_length=100)


class Appointment(models.Model):
    user = models.CharField(max_length=100)
    fullnames = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    date = models.CharField(max_length=100)
    timess = models.CharField(max_length=100)  
    address = models.CharField(max_length=100)
    DEPT = models.CharField(max_length=100)
    reason = models.CharField(max_length=100)

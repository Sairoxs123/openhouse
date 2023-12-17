from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Students(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    grade_sec = models.CharField("Class",max_length=3, null=False)
    jssid = models.CharField(max_length=12, blank=False, unique=True)

    def __str__(self):
        return self.jssid

class Teachers(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    name = models.CharField(max_length=50, blank=False, null=False)
    subject = models.CharField(max_length=30, blank=False, null=False)
    location = models.ImageField(upload_to='locations/', blank=True, null=True)

    def __str__(self):
        return self.name

class Reservations(models.Model):
    id = models.IntegerField(primary_key=True, blank=False, null=False, unique=True)
    student = models.ForeignKey(Students, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teachers, on_delete=models.CASCADE)
    time = models.TimeField(max_length=15, blank=False, null=False)

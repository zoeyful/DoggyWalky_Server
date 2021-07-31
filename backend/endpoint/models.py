from django.db import models
import datetime

# Create your models here.
class Account(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    pw = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    gender = models.CharField(max_length=2)
    phone_number = models.CharField(max_length=14)
    created_date = models.DateField(auto_now_add=True)

class Pet(models.Model):
    id =  models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    breed = models.CharField(max_length=30, null=True, blank=True)
    gender = models.CharField(max_length=3, null=True, blank=True)
    size = models.CharField(max_length=30, null=True, blank=True)
    created_date = models.DateField(auto_now_add=True, null=True, blank=True)
    profile_img = models.ImageField(upload_to='pet_profile', null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)

class WeightRecord(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    weight = models.CharField(max_length=10)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)

class ActivityRecord(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=40, null=True, blank=True)
    created_date = models.DateTimeField(default=datetime.datetime.now)
    activity_duration = models.CharField(max_length=40, null=True, blank=True)
    total_distnace = models.CharField(max_length=40, null=True, blank=True)
    gpx_file = models.CharField(max_length=200, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True, blank=True)

class Meal(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    item = models.CharField(max_length=200, null=True, blank=True)
    weight = models.CharField(max_length=30, null=True, blank=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.datetime.now)

class MealRecord(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    meal = models.ForeignKey(Meal, on_delete=models.DO_NOTHING)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.datetime.now)

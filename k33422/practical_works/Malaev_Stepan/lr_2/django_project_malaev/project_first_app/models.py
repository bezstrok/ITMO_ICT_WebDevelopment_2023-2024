from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


class Car(models.Model):
	id_car = models.AutoField(primary_key=True)
	state_number = models.CharField(max_length=14)
	brand = models.CharField(max_length=20)
	model = models.CharField(max_length=20)
	color = models.CharField(max_length=30, null=True)


class Driver(AbstractUser):
	id_driver = models.AutoField(primary_key=True)
	birth_date = models.DateField(null=True)
	cars = models.ManyToManyField(Car, through='Owning')
	passport_number = models.CharField(max_length=10, null=True)
	home_address = models.TextField(null=True)
	nationality = models.CharField(max_length=30, null=True)


class DriverLicense(models.Model):
	id_driver_license = models.AutoField(primary_key=True)
	id_car_owner = models.ForeignKey(get_user_model(), models.CASCADE)
	type = models.CharField(max_length=10)
	date_of_issue = models.DateField()


class Owning(models.Model):
	id_owning = models.AutoField(primary_key=True)
	id_car_owner = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True)
	id_car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
	start_date = models.DateField()
	end_date = models.DateField(null=True)

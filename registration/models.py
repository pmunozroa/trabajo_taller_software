from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.


class User(AbstractUser):
    is_person = models.BooleanField(default=False)
    is_municipality = models.BooleanField(default=False)


# Set email as UNIQUE
User._meta.get_field('email')._unique = True


class Country(models.Model):
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class City(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_id_user = models.CharField(max_length=12, unique=True)
    middle_name = models.CharField(max_length=25)
    sur_name = models.CharField(max_length=25)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class Municipality(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_id_municipality = models.CharField(max_length=12, unique=True)
    name_municipality = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.OneToOneField(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_municipality

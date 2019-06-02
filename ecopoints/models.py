from django.db import models
from registration.models import Country, City
from django.utils import timezone
from registration.models import Person, Municipality
# Create your models here.


class RecyclingPoint(models.Model):
    real_id_point = models.CharField(
        max_length=12, unique=True, verbose_name='RUT de la Empresa')
    name_point = models.CharField(
        max_length=50, verbose_name='Nombre de la empresa')
    address_point = models.CharField(
        max_length=100, verbose_name='Dirección de la empresa')
    latitude_point = models.FloatField()
    longitude_point = models.FloatField()
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,
                                verbose_name='Región en que está situada la empresa')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             verbose_name='Comuna en que está situada la empresa')
    is_active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Punto de reciclaje'
        verbose_name_plural = 'Puntos de reciclaje'


class RecyclingPointRequest(models.Model):
    request_date = models.DateTimeField(auto_now_add=True, editable=False)
    request_approbation_date = models.DateTimeField(auto_now=True, null=True)
    was_evaluated = models.BooleanField(default=False)
    was_approved = models.BooleanField(default=False)
    request_user = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True)
    request_municipality = models.ForeignKey(
        Municipality, on_delete=models.SET_NULL, null=True)
    request_recyclingpoint = models.ForeignKey(
        RecyclingPoint, on_delete=models.CASCADE)

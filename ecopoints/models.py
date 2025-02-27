from django.db import models
from registration.models import Country, City
from django.utils import timezone
from registration.models import Person, Municipality
from django.core.validators import RegexValidator
# Create your models here.


class RecyclingPoint(models.Model):
    
    """
    Almacena un nuevo punto de reciclaje, relacionado a :model:`registration.City` y :model:`registration.Country`.
    """
    
    real_id_point = models.CharField(
        max_length=12, unique=True, verbose_name='RUT de la Empresa', validators=[
            RegexValidator(
                regex='^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$',
                message='RUT Incorrecto',
            ),
        ])
    name_point = models.CharField(
        max_length=50, verbose_name='Nombre de la empresa')
    address_point = models.CharField(
        max_length=100, verbose_name='Dirección de la empresa')
    latitude_point = models.FloatField(verbose_name='Latitud', help_text='Ingrese los valores con puntos para separar decimales')
    longitude_point = models.FloatField(verbose_name='Longitud', help_text='Ingrese los valores con puntos para separar decimales')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True,
                                verbose_name='Región en que está situada la empresa')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True,
                             verbose_name='Comuna en que está situada la empresa')
    is_active = models.BooleanField(default=False, verbose_name='Punto activo')

    class Meta:
        verbose_name = 'Punto de reciclaje'
        verbose_name_plural = 'Puntos de reciclaje'


class RecyclingPointRequest(models.Model):
    
    """
    Almacena un registro de solicitud nuevo punto de reciclaje, relacionado a :model:`registration.Person`, :model:`registration.Municipality` y :model:`ecopoints.RecyclingPoint`.
    """
    
    request_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='Fecha de solicitud')
    request_approbation_date = models.DateTimeField(auto_now=True, null=True, verbose_name='Fecha de aprobación')
    was_evaluated = models.BooleanField(default=False, verbose_name='Fue evaluado')
    was_approved = models.BooleanField(default=False, verbose_name='Fue aprobado')
    request_user = models.ForeignKey(
        Person, on_delete=models.SET_NULL, null=True)
    request_municipality = models.ForeignKey(
        Municipality, on_delete=models.SET_NULL, null=True)
    request_recyclingpoint = models.ForeignKey(
        RecyclingPoint, on_delete=models.CASCADE)

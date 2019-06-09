from django.db import models
from django.contrib.auth.models import AbstractUser, User
# Create your models here.


class User(AbstractUser):
    
    """
    Extiende al usuario base de Django para añadirle nuevos campos para poder crear diferentes tipos de usuario.
    """
    
    is_person = models.BooleanField(default=False, verbose_name='Es una persona - Indica si el usuario es persona o empresa dentro del sitio')
    is_municipality = models.BooleanField(default=False, verbose_name='Es una municipalidad - Indica si el usuario es municipalidad dentro del sitio')


# Set email as UNIQUE
User._meta.get_field('email')._unique = True


class Country(models.Model):
    
    """
    Almacena un registro de regiones de Chile, poblada manualmente.
    """
    
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name


class City(models.Model):
    
    """
    Almacena un registro de comunas de Chile, poblada manualmente, relacionada a :model:`registration.Country`.
    """
    
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    name = models.CharField(max_length=80)
    latitude = models.FloatField(verbose_name='Latitud - Coordenadas Latitudinales')
    longitude = models.FloatField(verbose_name='Longitud - Coordenadas Longitudinales')

    def __str__(self):
        return self.name


class Person(models.Model):
     
    """
    Almacena un registro de un usuario tipo Persona, relacionada a :model:`registration.User`.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_id_user = models.CharField(max_length=12, unique=True, verbose_name='RUN de la persona - Rol Unico Nacional, valor único para evitar multicuentas.')
    middle_name = models.CharField(max_length=25, verbose_name='Segundo Nombre')
    sur_name = models.CharField(max_length=25, verbose_name='Segundo Apellido')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)


class Municipality(models.Model):
     
    """
    Almacena un registro de un usuario tipo Municipalidad, relacionada a :model:`registration.User`.
    """
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    real_id_municipality = models.CharField(max_length=12, unique=True, verbose_name='RUT de la Municipalidad - Rol Unico Tributario')
    name_municipality = models.CharField(max_length=100, verbose_name='Nombre de la municipalidad')
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True)
    city = models.OneToOneField(City, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name_municipality

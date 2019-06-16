from django import forms
from django.core.exceptions import ValidationError

from .models import RecyclingPoint


class RecyclingPointForm(forms.ModelForm):
    class Meta:
        model = RecyclingPoint
        fields = ('real_id_point', 'name_point', 'address_point',
              'latitude_point', 'longitude_point')
    
    def clean_real_id_point(self):
        if RecyclingPoint.objects.filter(real_id_point=self.cleaned_data['real_id_point']).exists():
            raise forms.ValidationError("El rut ya se encuentra registrado")
        return self.cleaned_data['real_id_point']

    def clean_latitude_point(self):
        if self.cleaned_data['latitude_point'] > 90 or self.cleaned_data['latitude_point'] < -90:
            raise forms.ValidationError("La Latitud debe ser entre -90 y 90")
        return self.cleaned_data['latitude_point']
    
    def clean_longitude_point(self):
        if self.cleaned_data['longitude_point'] > 180 or self.cleaned_data['longitude_point'] < -180:
            raise forms.ValidationError("La Longitud debe ser entre -180 y 180")
        return self.cleaned_data['longitude_point']
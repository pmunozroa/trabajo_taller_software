from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
import re
from .models import Person, City, Country, User, Municipality
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _


class PersonSignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(PersonSignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['real_id_user'].widget.attrs.update({'autofocus': 'autofocus'})

    last_name = forms.CharField(required=True, label='Primer apellido')
    real_id_user = forms.CharField(required=True, max_length=12, label='RUN', validators=[
        RegexValidator('^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$')], help_text="Formato: 12.345.678-K")
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
                                     widget=forms.Select, required=True, label='Región')
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select, required=True, label='Comuna')
    middle_name = forms.CharField(
        max_length=25, required=False, label='Segundo nombre', help_text="Opcional")
    sur_name = forms.CharField(max_length=25, label='Segundo apellido')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "first_name",
                  "last_name", "email", "password1", "password2")

    field_order = ['real_id_user', 'first_name', 'middle_name', 'last_name', 'sur_name', 'country', 'city',
                   'email', 'username', 'password1', 'password2']

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_person = True
        user.save()
        person = Person.objects.create(user=user)
        person.real_id_user = self.cleaned_data.get('real_id_user')
        person.middle_name = self.cleaned_data.get('middle_name')
        person.sur_name = self.cleaned_data.get('sur_name')
        person.country = self.cleaned_data.get('country')
        person.city = self.cleaned_data.get('city')
        person.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("El correo ya se encuentra en uso")
        return self.cleaned_data['email']

    def clean_real_id_user(self):
        if Person.objects.filter(real_id_user=self.cleaned_data['real_id_user']).exists():
            raise forms.ValidationError("El rut ya se encuentra registrado")
        return self.cleaned_data['real_id_user']


class MunicipalitySignUpForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(MunicipalitySignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.pop("autofocus", None)
        self.fields['real_id_municipality'].widget.attrs.update({'autofocus': 'autofocus'})

    real_id_municipality = forms.CharField(required=True, max_length=12, label='RUT', validators=[
        RegexValidator('^\d{1,2}\.\d{3}\.\d{3}[-][0-9kK]{1}$')], help_text="Formato: 70.000.000-K")
    name_municipality = forms.CharField(
        required=True, max_length=100, label='Nombre municipalidad')
    country = forms.ModelChoiceField(queryset=Country.objects.all(),
                                     widget=forms.Select, required=True, label='Región')
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select, required=True, label='Comuna')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "password1", "password2")

    field_order = ['real_id_municipality', 'name_municipality', 'country', 'city',
                   'email', 'username', 'password1', 'password2']

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_municipality = True
        user.save()
        municipality = Municipality.objects.create(user=user)
        municipality.real_id_municipality = self.cleaned_data.get(
            'real_id_municipality')
        municipality.name_municipality = self.cleaned_data.get(
            'name_municipality')
        municipality.country = self.cleaned_data.get('country')
        municipality.city = self.cleaned_data.get('city')
        municipality.save()
        return user

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("El correo ya se encuentra en uso")
        return self.cleaned_data['email']

    def clean_real_id_user(self):
        if Person.objects.filter(real_id_user=self.cleaned_data['real_id_municipality']).exists():
            raise forms.ValidationError("El rut ya se encuentra registrado")
        return self.cleaned_data['real_id_municipality']
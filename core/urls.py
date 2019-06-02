from django.urls import path
from .views import HomeView

core_patterns = ([
    path('', HomeView.as_view(), name='home'),
], 'core')

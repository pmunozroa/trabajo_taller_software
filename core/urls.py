from django.urls import path
from .views import HomeView, AboutView

core_patterns = ([
    path('', HomeView.as_view(), name='home'),
    path('about', AboutView.as_view(), name='about'),
], 'core')

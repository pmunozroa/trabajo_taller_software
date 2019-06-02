from django.urls import path
from .views import SignUpCreateView, PersonSignUpView, load_cities, MunicipalitySignUpView, LoginTemplateView, PersonDetailView, MunicipalityDetailView

registration_patterns = ([
    path('signup/', SignUpCreateView.as_view(), name='signup'),
    path('signup/person/', PersonSignUpView.as_view(), name='person_signup'),
    path('ajax/load-cities/', load_cities,
         name='ajax_load_cities'),
    path('signup/municipality/', MunicipalitySignUpView.as_view(),
         name='municipality_signup'),
    path('login/', LoginTemplateView.as_view(), name='login'),
    path('detail/person/<int:pk>/', PersonDetailView.as_view(), name='detail_user'),
    path('detail/municipality/<slug:city>/', MunicipalityDetailView.as_view(), name='detail_muni'),
], 'registration')

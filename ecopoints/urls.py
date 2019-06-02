from django.urls import path
from .views import RecyclingPointMapView, RecyclingPointCreateView, RecyclingPointListView, InactivesRecyclingPointListView, status_ecopoint, EvaluatedRecyclingPointRequestList, RecyclingPointDetailView

ecopoints_patterns = ([
    path('request/', RecyclingPointCreateView.as_view(), name='request'),
    path('points/', RecyclingPointListView.as_view(), name='points'),
    path('waiting/', InactivesRecyclingPointListView.as_view(), name='for_aprove'),
    path('ajax/change_recycling/', status_ecopoint,
         name='update_recycling_status'),
    path('history/', EvaluatedRecyclingPointRequestList.as_view(), name='history_request'),
    path('detail/<int:pk>/', RecyclingPointDetailView.as_view(), name='recycling_detail'),
    path('maps/', RecyclingPointMapView.as_view(), name='map_view'),
], 'ecopoints')

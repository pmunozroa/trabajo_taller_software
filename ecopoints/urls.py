from django.urls import path
from .views import (EvaluatedRecyclingPointRequestList,
                    InactivesRecyclingPointListView, RecyclingPointCreateView,
                    RecyclingPointDetailView, RecyclingPointListView,
                    RecyclingPointMapView, status_ecopoint, RecyclingPointDeleteView, RecyclingPointUpdateView)

ecopoints_patterns = ([
    path('request/', RecyclingPointCreateView.as_view(), name='request'),
    path('points/', RecyclingPointListView.as_view(), name='points'),
    path('waiting/', InactivesRecyclingPointListView.as_view(), name='for_aprove'),
    path('ajax/change_recycling/', status_ecopoint,
         name='update_recycling_status'),
    path('history/', EvaluatedRecyclingPointRequestList.as_view(), name='history_request'),
    path('detail/<int:pk>/', RecyclingPointDetailView.as_view(), name='recycling_detail'),
    path('maps/', RecyclingPointMapView.as_view(), name='map_view'),
    path('delete/<int:pk>/', RecyclingPointDeleteView.as_view(), name='delete_request'),
    path('update/<int:pk>/', RecyclingPointUpdateView.as_view(), name='update_point'),
], 'ecopoints')

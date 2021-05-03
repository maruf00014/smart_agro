# -*- encoding: utf-8 -*-
"""
License: MIT
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [
   
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/soil-data/<uuid:land_id>/', views.soil_data, name='soil-data'),
    path('dashboard/soil-data/<uuid:land_id>/<slug:date>/', views.soil_data_by_date, name='soil-data-by-date'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit-profile'),
    path('lands/', views.lands, name='lands'),
    path('add-land/', views.add_land, name='add-land'),
    path('edit-land/<uuid:land_id>/', views.edit_land, name='edit-land'),
    path('delete-land/<uuid:land_id>/', views.delete_land, name='delete-land'),
    path('maps/', views.maps, name='maps'),
    path('suggestion/', views.suggestion, name='suggestion'),
    path('suggestion/get-suggestion/<uuid:land_id>/', views.get_suggestion, name='get-suggestion'),
]

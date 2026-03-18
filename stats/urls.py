from django.urls import path
from . import views

urlpatterns = [
    path('', views.teams_list, name='home'),
    path('team/<int:team_id>/', views.team_detail, name='team_detail'),
    path('drivers/', views.drivers_list, name='drivers_list'),
    path('driver/<int:driver_id>/', views.driver_detail, name='driver_detail'),
    path('compare/', views.driver_compare, name='driver_compare'),
    path('races/', views.races_list, name='races_list'),
]

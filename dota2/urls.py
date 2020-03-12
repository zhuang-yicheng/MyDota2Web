from django.urls import path
from . import views

urlpatterns = [
    path('public_details/team', views.team, name = 'team'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('index', views.index, name = 'index'),
    path('pyecharts_test1', views.pyecharts_test1, name = 'pyecharts_test1'),
]
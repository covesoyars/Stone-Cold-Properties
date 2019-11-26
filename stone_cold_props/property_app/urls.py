from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table, name='table'),
    path('search/', views.search, name='search'),
    path('results/', views.search_results, name='search_results'),
    ]
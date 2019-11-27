from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('table/', views.table, name='table'),
    path('search_by_address/', views.search_by_address, name='search_by_address'),
    path('results_by_address/', views.results_by_address, name='results_by_address'),
    path('expiring_contracts_search/', views.expiring_contracts_search, name='expiring_contracts_search')
    ]
from django.urls import path

from . import views

urlpatterns = [
    path('', views.signIn, name='signIn'),
    path('table/', views.table, name='table'),
    path('search_by_address/', views.search_by_address, name='search_by_address'),
    path('results_by_address/', views.results_by_address, name='results_by_address'),
    path('expiring_contracts_search/', views.expiring_contracts_search, name='expiring_contracts_search'),
    path('expiring_contracts_results/', views.expiring_contracts_results, name='expiring_contracts_results'),
    path('tenant_search/', views.tentant_search, name='tenant_search'),
    path('tenant_search_results/', views.tenant_search_results, name='tenant_search_results'),
    path('property_manager_search_address/', views.property_manager_search_by_address, name='property_manager_search_address'),
    path('manager_results_address/', views.manager_results_by_address, name='manager_results_address'),
    path('property_manager_search_owner/', views.manager_search_by_owner, name='search_manager_owner'),
    path('manager_results_owner', views.manager_results_by_owner, name='manager_results_owner'),
    path('building_search/', views.building_search, name='building_search'),
    path('building_results/', views.building_results, name='building_results'),
	path('admin_sql/', views.admin_sql_bar, name='admin_sql'),
    path('sql_results/', views.sql_results, name='sql_results'),
    path('adminPage/', views.admin_page, name='admin_page'),
    path('employee_page/', views.employee_page, name='employee_page'),

    ]
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'banking_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('activity/<account_id>', views.activity, name='activity'),
    path('transfers/<account_id>', views.transfers, name='transfers'),
    path('employee/', views.employee, name='employee'),
    path('add_customer', views.add_customer, name='add_customer'),
    path('add_account', views.add_account, name='add_account'),
    path('edit_customer/<customer_id>', views.edit_customer, name='edit_customer'),
]
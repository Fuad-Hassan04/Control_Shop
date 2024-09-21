from django.urls import path
from .views import *

urlpatterns =[
path('', index, name='index'),
path('create-customar/', add_customar, name='add_customar'),
path('add or/', add_or, name='add_or'),
path('sign_up/', sign_up, name='sign_up'),
path('signin/', sign_in, name='sign_in'),
path('signout/', sign_out, name='sign_out'),
path('user_profile/', user_profile, name='user_profile'),
path('customar_list/', customar_list, name='customar_list'),
path('total_cost/', total_costs, name='total_cost'),

path('update-customer/<int:customer_id>/', update_customer, name='update_customer'),
path('customar_detail/', customar_detail_by_modal, name='customar_detail'),
path('delete_customar/', delete_customar, name='delete_customar'),



]
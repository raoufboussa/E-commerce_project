from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.Item_liste, name='home'),
    path('product/', views.Product, name='product'),
    path('checkout/', views.Checkout, name='checkout'),
]

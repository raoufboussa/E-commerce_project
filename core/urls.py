from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeProduct.as_view(), name='home'),
    path('product/<slug>/', views.DetailProduct.as_view(), name='product'),
    path('checkout/', views.Checkout, name='checkout'),
]

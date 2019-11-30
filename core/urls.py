from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeProduct.as_view(), name='home'),
    path('product/<slug>/', views.DetailProduct.as_view(), name='product'),
    path('checkout/', views.Checkout, name='checkout'),
    path('order_summary', views.OrderSummaryView.as_view(), name='order_summary'),
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/',
         views.remove_from_cart, name='remove_from_cart'),
]

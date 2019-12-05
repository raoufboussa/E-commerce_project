from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeProduct.as_view(), name='home'),
    path('product/<slug>/', views.DetailProduct.as_view(), name='product'),
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('order_summary', views.OrderSummaryView.as_view(), name='order_summary'),
    path('add_coupon/', views.Add_Coupon.as_view(), name='add_coupon'),
    path('add_to_cart/<slug>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<slug>/',
         views.remove_from_cart, name='remove_from_cart'),
    path('remove_from_cart_quantity/<slug>/', views.remove_from_cart_quantity,
         name='remove_from_cart_quantity'),
    path('payment/<payment_option>', views.PaymentView.as_view(), name='payment'),

]

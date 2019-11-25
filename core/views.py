from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Item


def Checkout(request):
    context = {
        "Items": Item.objects.all()
    }
    return render(request, "checkout-page.html", context)


# def Product(request):
#   context = {
#      "Items": Item.objects.all()
# }
# return render(request, "product-page.html", context)


class HomeProduct(ListView):
    model = Item
    template_name = 'home-page.html'


# def Item_liste(request):
#   context = {
#       "Items": Item.objects.all()
#   }
#   return render(request, "home-page.html", context)


class DetailProduct(DetailView):
    model = Item
    template_name = 'product-page.html'

from django.shortcuts import render
from .models import Item


def Item_liste(request):
    context = {
        "Items": Item.objects.all()
    }
    return render(request, "home-page.html", context)


def Product(request):
    context = {
        "Items": Item.objects.all()
    }
    return render(request, "product-page.html", context)


def Checkout(request):
    context = {
        "Items": Item.objects.all()
    }
    return render(request, "checkout-page.html", context)

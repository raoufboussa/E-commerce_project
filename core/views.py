from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from django.utils import timezone
from .models import Item, Order, OrderItem


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


def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # si le order item est dans order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, 'this item quantity was apdated seccesfully')
            return redirect("core:product", slug=slug)
        else:
            order.items.add(order_item)
            messages.info(
                request, 'the item was added seccesfully to yout cart')
            return redirect("core:product", slug=slug)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'the item was added seccesfully to yout cart')
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)


def remove_from_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order_item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False
            )[0]
            order.items.remove(order_item)
            messages.info(request, 'the item was removed from your cart')
            return redirect("core:product", slug=slug)
        else:
            messages.info(request, 'you do not have this item in your cart')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'you do not have any active order')
        return redirect("core:product", slug=slug)
    return redirect("core:product", slug=slug)

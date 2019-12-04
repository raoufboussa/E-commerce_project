from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, View
from django.utils import timezone
from .models import Item, Order, OrderItem, Billing, Payment
from django.core.paginator import Paginator
from .forms import CheckoutForm
import stripe
import logging
stripe.api_key = settings.STRIPE_SECRET_KEY


class Checkout(View):
    def get(self, *args, **kwargs):
        form = CheckoutForm()
        context = {
            "form": form
        }
        return render(self.request, "checkout-page.html", context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get("street_address")
                apartment_address = form.cleaned_data.get("apartment_address")
                country = form.cleaned_data.get("country")
                zip = form.cleaned_data.get("zip")
                # TODO: add fonctionality for these fields
                # same_billing_address = form.cleaned_data.get(
                #     "same_billing_address")
                # save_info = form.cleaned_data.get("save_info")
                payment_option = form.cleaned_data.get("payment_option")
                billing = Billing(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    country=country,
                    zip=zip,
                    # TODO:add some fonctionality for these fields
                    # same_billing_address=same_billing_address,
                    # save_info=save_info,
                    # payment_option=payment_option,
                )
                billing.save()
                order.billing = billing
                order.save()
                return redirect('core:checkout')
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("core:order_summary")

        messages.warning(self.request, "Failed Checkout")
        return redirect('core:checkout')


class HomeProduct(ListView):
    model = Item
    paginate_by = 10
    template_name = 'home-page.html'


class OrderSummaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'objects': order
            }
            return render(self.request, 'order_summary.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "you do not have an active order")
            return redirect("/")


class DetailProduct(DetailView):
    model = Item
    template_name = 'product-page.html'


@login_required
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
        # if the order_item is in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(
                request, 'this item quantity was apdated seccesfully')
            return redirect("core:order_summary")
        else:
            order.items.add(order_item)
            messages.info(
                request, 'the item was added seccesfully to yout cart')
            return redirect("core:order_summary")
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(
            user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'the item was added seccesfully to yout cart')
        return redirect("core:order_summary")


@login_required
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
            order_item.quantity = 1
            order_item.save()
            order.items.remove(order_item)
            messages.info(request, 'the item was removed from your cart')
            return redirect("core:order_summary")
        else:
            messages.info(request, 'you do not have this item in your cart')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'you do not have any active order')
        return redirect("core:product", slug=slug)


@login_required
def remove_from_cart_quantity(request, slug):
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
            order_item.quantity -= 1
            if order_item.quantity == 0:
                order.items.remove(order_item)
                messages.info(request, 'the item was removed from your cart')
                return redirect("core:order_summary")
            order_item.save()
            messages.info(request, 'the item Quantity was updated')
            return redirect("core:order_summary")
        else:
            messages.info(request, 'you do not have this item in your cart')
            return redirect("core:product", slug=slug)
    else:
        messages.info(request, 'you do not have any active order')
        return redirect("core:product", slug=slug)


class PaymentView(View):
    def get(self, *args, **kwargs):
        # order
        return render(self.request, "payment.html")

    def post(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        token = self.request.POST.get('stripeToken')
        amount = int(order.get_total() * 100)  # cents

        try:
            charge = stripe.Charge.create(
                currency="usd",
                source=token,
                amount=amount
            )

            # Create the payment
            payment = Payment()
            payment.stripe_charge_id = charge['id']
            payment.user = self.request.user
            payment.amount = order.get_total()
            payment.save()

            # assing the payment into the order
            order.ordered = True
            order.payment = payment
            order.save()

            messages.success(self.request, "Your order was seccessful!")
            return redirect("/")

        except stripe.error.CardError as e:
            # body = e.json_body
            # err = body.get('error', {})
            # messages.error(self.request, f"{err.get('message')}")
            # return redirect("/")
            print('Status is: %s' % e.http_status)
            print('Type is: %s' % e.error.type)
            print('Code is: %s' % e.error.code)
            # param is '' in this case
            print('Param is: %s' % e.error.param)
            print('Message is: %s' % e.error.message)
        except stripe.error.RateLimitError as e:
            # Too many requests made to the API too quickly
            messages.error(self.request, "Rate limit error.")
            return redirect("/")
        except stripe.error.InvalidRequestError as e:
            # Invalid parameters were supplied to Stripe's API
            messages.error(self.request, "Invalid parameters.")
            return redirect("/")
        except stripe.error.AuthenticationError as e:
            # Authentication with Stripe's API failed
            # (maybe you changed API keys recently)
            messages.error(self.request, "Not authenticated.")
            return redirect("/")
        except stripe.error.APIConnectionError as e:
            # Network communication with Stripe failed
            messages.error(self.request, "Network error.")
            return redirect("/")
        except stripe.error.StripeError as e:
            # Display a very generic error to the user, and maybe send
            # yourself an email
            messages.error(
                self.request, "Somthing went wrong. You were not charged. Please try again.")
            return redirect("/")
        except Exception as e:
            # send an email to ourselves
            messages.error(
                self.request, "A serious error occured. You have been notifed. ")
            return redirect("/")

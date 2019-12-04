from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from cities_light import city_items_pre_import

PAYMENT_CHOICES = {
    ('PL', 'Paypal'),
    ('PR', 'Paysera'),
    ('DH', 'Dahabiya'),
}


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': '1234 Main St',
        'class': 'form-control',
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment or suit',
        'class': 'form-control',
    }))
    country = CountryField(blank_label="(select country)").formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100',

    }))
    # state = (blank_label="(select country)").formfield(attrs={
    # 'class': 'custom-select d-block w-100'
    # })
    zip = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'placeholder': 'Zip',
        'class': 'form-control',
    }))
    same_billing_address = forms.BooleanField(required=False)
    save_info = forms.BooleanField(required=False)
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect(), choices=PAYMENT_CHOICES)

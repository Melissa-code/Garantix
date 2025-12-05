from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Warranty


class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class WarrantyForm(forms.ModelForm):
    class Meta:
        model = Warranty
        fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes"]
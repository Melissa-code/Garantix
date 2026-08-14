from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Warranty


class CustomUserCreationForm(UserCreationForm):
    """ Formulaire de création d'utilisateur personnalisé qui utilise l'email comme nom d'utilisateur"""
    username: forms.EmailField = forms.EmailField(label="Email", required=True)

    class Meta:
        model: type[User] = User
        fields: tuple[str, ...] = ("username", "password1", "password2")


class WarrantyForm(forms.ModelForm):
    """ Formulaire pour créer ou mettre à jour une garantie """
    class Meta:
        model: type[Warranty] = Warranty
        fields: list[str] = [
            "product_name", 
            "brand", 
            "purchase_date", 
            "warranty_duration_months", 
            "vendor", 
            "imageReceipt", 
            "notes"
        ]
        error_messages: dict[str, dict[str, str]] = {
            'product_name': {
                'min_length': "Le nom est trop court.",
                'max_length': "Le nom est trop long.",
            },
            'brand': {
                'min_length': "La marque est trop courte.",
                'max_length': "La marque est trop longue.",
            },
            'warranty_duration_months': {
                'min_value': "La durée doit être un nombre positif.",
                'max_value': "La durée est trop longue.",
            },
            'vendor': {
                'max_length': "Le nom du revendeur est trop long.",
            },
        }
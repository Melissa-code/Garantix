from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re


class CustomUserCreationForm(UserCreationForm):
    """
    Create 3 required fields (username = email unique)
    - validation password via regex 
    """
    username = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


    def clean_username(self):
        """
        Vérifie que l'email n'est pas déjà utilisé
        """
        email = self.cleaned_data.get("username")
        
        if User.objects.filter(username=email).exists():
            raise ValidationError("Un compte avec cet email existe déjà.")
        return email

    def clean_password1(self):
        """
        Check complexity of password (8 char, 1 maj, 1 number, 1 symbole)
        """
        password = self.cleaned_data.get("password1")
        pattern = r'^(?=.*[A-Z])(?=.*\d)(?=.*[-_!@#$%^&*]).+$'

        if not re.match(pattern, password):
            raise ValidationError("Le mot de passe doit contenir une majuscule, un chiffre et un symbole.")
        
        if len(password) < 8:
            raise ValidationError("Le mot de passe doit contenir au moins 8 caractères.")
        
        return password
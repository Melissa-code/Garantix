from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    username = forms.EmailField(label="Email", required=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import CustomUserCreationForm
# from django.contrib.auth.forms import UserCreationForm


@method_decorator(login_required, name="dispatch")
class CustomLogoutView(View): 
    """
    Déconnecte l'utilisateur + le redirige vers la page d'accueil
    - supprime la session de l'utilisateur + affiche un message de confirmation
    """
    def get(self, request): 
        logout(request)
        messages.success(request, "Vous êtes déconnecté.")

        return redirect('warranty:home')


class SignupView(CreateView):
    """ 
    Crée un compte utilisateur
    - le redirige vers la page de connexion
    """
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("accounts:login") 

    def form_valid(self, form, request): 
        # appelle form.save() : create user DB
        response = super().form_valid(form)
        login(self.request, self.object)

        return response
    
    # TODO : logs
    def form_invalid(self, form):
        print("Formulaire INVALIDE")
        print("Erreurs:", form.errors)
        print("POST data:", self.request.POST)
        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """ 
    Connecte l'utilisateur 
    - le redirige vers la page Liste des garanties
    """
    template_name = "login.html"
    
    def get_success_url(self):
        return reverse_lazy('warranty:warranties_list')

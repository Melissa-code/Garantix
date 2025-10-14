from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout, login, authenticate
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib import messages
from .forms import CustomUserCreationForm


@method_decorator(login_required, name="dispatch")
class CustomLogoutView(View): 
    """
    Déconnecte l'utilisateur + le redirige vers la page d'accueil
    - supprime la session de l'utilisateur + affiche un message de confirmation
    """
    def get(self, request): 
        logout(request)
        messages.success(request, "Déconnexion effectuée. A bientôt !")

        return redirect('warranty:home')


class SignupView(CreateView):
    """ 
    Crée un compte utilisateur
    - le redirige vers la page de connexion + affiche un message de succès/erreur 
    """
    form_class = CustomUserCreationForm
    template_name = "signup.html"
    success_url = reverse_lazy("warranty:home") 

    def form_valid(self, form): 
        """appelle form.save(): create user DB"""
        response = super().form_valid(form)
        login(self.request, self.object)
        messages.success(self.request, "Bienvenue ! Votre compte a été créé avec succès.")

        return response
    
    # TODO : logs
    def form_invalid(self, form):
        messages.error(self.request, "Erreur lors de la création du compte. Vérifiez les informations.")

        return super().form_invalid(form)


class CustomLoginView(LoginView):
    """ 
    Connecte l'utilisateur 
    - le redirige vers la page Liste des garanties
    """
    template_name = "login.html"
    
    def form_valid(self, form):
        user = form.get_user()
        messages.success(self.request, f"Bienvenue {user.get_full_name() or user.username} !")
        return super().form_valid(form)
   
    def get_success_url(self):
        return reverse_lazy('warranty:warranties_list')

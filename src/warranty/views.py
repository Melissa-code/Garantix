from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from warranty.models import Warranty
from warranty.mixins import ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin
from .forms import WarrantyForm


class HomeView(TemplateView): 
    """Accueil - redirige vers la liste des garanties si connecté sinon affiche une page d'accueil"""
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context


class WarrantiesListView(LoginRequiredMixin, ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin, ListView):
    """Liste des garanties de l'utilisateur connecté avec barre de recherche"""
    model = Warranty
    context_object_name = "warranties" 
    template_name = "warranty/warranties_list.html"


class WarrantyDetailView(LoginRequiredMixin, UserWarrantyMixin, DetailView):
    """Page Détail de la garantie - affiche les détails d'une garantie spécifique"""
    model = Warranty
    context_object_name = "warranty"
    template_name = "warranty/warranty_detail.html"
  

class WarrantyCreateView(LoginRequiredMixin, UserWarrantyMixin, CreateView):
    """Page Créer une nouvelle garantie - formulaire pour ajouter une nouvelle garantie"""
    model = Warranty
    form_class = WarrantyForm
    template_name = "warranty/warranty_create.html"

    def form_valid(self, form):
        """Assigne l'utilisateur connecté à la nouvelle garantie"""
        form.instance.user = self.request.user
        return super().form_valid(form)


class WarrantyUpdateView(LoginRequiredMixin, UserWarrantyMixin, UpdateView):
    """Page Modifier une garantie - formulaire pré-rempli pour éditer une garantie existante"""
    model = Warranty
    form_class = WarrantyForm
    template_name = "warranty/warranty_update.html"
        
        
class WarrantyDeleteView(LoginRequiredMixin, UserWarrantyMixin, DeleteView):
    """Page Supprimer une garantie - confirmation avant de supprimer une garantie existante"""
    model = Warranty
    context_object_name = "warranty"
    success_url = reverse_lazy("warranty:warranties_list")
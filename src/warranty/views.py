from django.db import IntegrityError
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from warranty.models import Warranty
from warranty.mixins import ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin
from warranty.forms import WarrantyForm
from warranty import services
from django.http import JsonResponse
from django.contrib import messages


class HomeView(TemplateView): 
    """Accueil - redirige vers la liste des garanties si connecté sinon affiche une page d'accueil"""
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context


class WarrantiesListView(LoginRequiredMixin, ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin, ListView):
    """Liste des garanties de l'utilisateur connecté avec barre de recherche"""
    context_object_name = "warranties" 
    template_name = "warranty/warranties_list.html"
    paginate_by = 3

    def get_queryset(self):
        """Récupère les garanties de l'utilisateur connecté filtrées par la barre de recherche"""
        queryset = services.get_user_warranties(user=self.request.user)
        self.queryset = queryset 
        return super().get_queryset()


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
        product = form.cleaned_data.get('product_name')
        brand = form.cleaned_data.get('brand')
        user = self.request.user
        exists = Warranty.objects.filter(user=user, product_name=product, brand=brand).exists()

        if exists:
            messages.error(self.request, "Ce produit est déjà enregistré pour cette marque.")
            return self.form_invalid(form)

        form.instance.user = user
        messages.success(self.request, "Garantie ajoutée avec succès.")
        return super().form_valid(form)
   

class WarrantyUpdateView(LoginRequiredMixin, UserWarrantyMixin, UpdateView):
    """Page Modifier une garantie - formulaire pré-rempli pour éditer une garantie existante"""
    model = Warranty
    form_class = WarrantyForm
    template_name = "warranty/warranty_update.html"

    def form_valid(self, form):
        product = form.cleaned_data.get('product_name')
        brand = form.cleaned_data.get('brand')
        user = self.request.user
        duplicate = Warranty.objects.filter(
            user=user, 
            product_name__iexact=product, 
            brand__iexact=brand
        ).exclude(pk=self.object.pk).exists()

        if duplicate:
            messages.error(self.request, "Une garantie existe déjà avec ce nom et cette marque.")
            form.add_error('product_name', "Ce nom est déjà utilisé pour cette marque.")
            return self.form_invalid(form)

        messages.success(self.request, "Garantie modifiée avec succès.")
        return super().form_valid(form)

        
        
class WarrantyDeleteView(LoginRequiredMixin, UserWarrantyMixin, DeleteView):
    """Page Supprimer une garantie - confirmation avant de supprimer une garantie existante"""
    model = Warranty
    context_object_name = "warranty"
    success_url = reverse_lazy("warranty:warranties_list")
   
    def form_valid(self, form):
        product_name = self.object.product_name
        self.object.delete()
        
        # req AJAX pour supprimer la garantie sans recharger la page
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'status': 'success',
                'message': f'Garantie "{product_name}" supprimée avec succès'
            })
        return super().form_valid(form)

    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'status': 'error', 'message': 'Erreur lors de la suppression.'}, status=400)
        return super().form_invalid(form)

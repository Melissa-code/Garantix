from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from warranty.models import Warranty
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import redirect
from django.views import View
from django.db.models import Q
from warranty.mixins import ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin
from .forms import WarrantyForm


class HomeView(TemplateView): 
    """Accueil - redirige vers la liste des garanties si connecté sinon affiche une page d'accueil"""
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context


@method_decorator(login_required, name="dispatch")
class WarrantiesListView(ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin, ListView):
    """Liste des garanties de l'utilisateur connecté avec barre de recherche"""
    model = Warranty
    context_object_name = "warranties" # variable in template
    template_name = "warranty/warranties_list.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", "created_at", ]


@method_decorator(login_required, name="dispatch")
class WarrantyDetailView(UserWarrantyMixin, DetailView):
    """Page Détail de la garantie - affiche les détails d'une garantie spécifique"""
    model = Warranty
    context_object_name = "warranty"
    template_name = "warranty/warranty_detail.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", "created_at", ]


@method_decorator(login_required, name="dispatch")
class WarrantyCreateView(UserWarrantyMixin, CreateView):
    """Page Créer une nouvelle garantie - formulaire pour ajouter une nouvelle garantie"""
    model = Warranty
    template_name = "warranty/warranty_create.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", ]

    def form_valid(self, form):
        """Assigne l'utilisateur connecté à la nouvelle garantie"""
        form.instance.user = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name="dispatch")
class WarrantyUpdateView(UserWarrantyMixin, UpdateView):
    """Page Modifier une garantie - formulaire pré-rempli pour éditer une garantie existante"""
    model = Warranty
    template_name = "warranty/warranty_update.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", ]
    # success_url = reverse_lazy('warranty:warranties_list')
        
    def post(self, request, *args, **kwargs):
        """Surcharge pour forcer la prise en compte des fichiers"""
        return super().post(request, *args, **kwargs)
    
    def form_valid(self, form):
        # Si un nouveau fichier est uploadé, l'assigner manuellement
        if 'imageReceipt' in self.request.FILES:
            form.instance.imageReceipt = self.request.FILES['imageReceipt']
            # print(" Nouvelle image assignée!")
        
        return super().form_valid(form)
    
        
@method_decorator(login_required, name="dispatch")
class WarrantyDeleteView(UserWarrantyMixin, DeleteView):
    """Page Supprimer une garantie - confirmation avant de supprimer une garantie existante"""
    model = Warranty
    context_object_name = "warranty"
    success_url = reverse_lazy("warranty:home")
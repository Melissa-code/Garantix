from django.db.models import QuerySet
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
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from warranty.constants import FEATURES_HOME, MOCKUPS_HOME, TESTIMONIALS_HOME
from typing import Any, Dict
from typing import Type
from django.template.loader import render_to_string


class HomeView(TemplateView):
    """Accueil - redirige vers la liste des garanties si connecté sinon affiche une page d'accueil"""
    template_name: str = "warranty/home.html"

    def get_context_data(self, **kwargs) -> Dict[str, Any]:
        context: Dict[str, Any] = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        context['features'] = FEATURES_HOME
        context['mockups'] = MOCKUPS_HOME
        context['testimonials'] = TESTIMONIALS_HOME
        return context


class WarrantiesListView(LoginRequiredMixin, ContextDataMixin, WarrantySearchMixin, UserWarrantyMixin, ListView):
    """Liste des garanties de l'utilisateur connecté avec barre de recherche"""
    context_object_name: str = "warranties"
    template_name: str = "warranty/warranties_list.html"
    paginate_by: int = 3

    def get_queryset(self) -> QuerySet[Warranty]:
        """Récupère les garanties de l'utilisateur connecté filtrées par la barre de recherche"""
        queryset: QuerySet[Warranty] = services.get_user_warranties(user=self.request.user)
        self.queryset = queryset
        return super().get_queryset()


class WarrantyDetailView(LoginRequiredMixin, UserWarrantyMixin, DetailView):
    """Page Détail de la garantie - affiche les détails d'une garantie spécifique"""
    model: Type[Warranty] = Warranty
    context_object_name: str = "warranty"
    template_name: str = "warranty/warranty_detail.html"
  

class WarrantyCreateView(LoginRequiredMixin, UserWarrantyMixin, CreateView):
    """Page Créer une nouvelle garantie - formulaire pour ajouter une nouvelle garantie"""
    model: Type[Warranty] = Warranty
    form_class: Type[WarrantyForm] = WarrantyForm
    template_name: str = "warranty/warranty_create.html"

    def form_valid(self, form) -> HttpResponse:
        product: str = form.cleaned_data.get('product_name')
        brand: str = form.cleaned_data.get('brand')
        user = self.request.user
        
        # vérification doublon pour le même utilisateur, produit et marque
        exists: bool = Warranty.objects.filter(user=user, product_name=product, brand=brand).exists()
        if exists:
            messages.error(self.request, "Ce produit est déjà enregistré pour cette marque.")
            return self.form_invalid(form)

        form.instance.user = user

        try: 
            response = super().form_valid(form)
            messages.success(self.request, "Garantie ajoutée avec succès.")
            return response
        except Exception :
            messages.error(self.request, f"Erreur lors de l'ajout de la garantie.")
            return self.form_invalid(form)


class WarrantyUpdateView(LoginRequiredMixin, UserWarrantyMixin, UpdateView):
    """Page Modifier une garantie - formulaire pré-rempli pour éditer une garantie existante"""
    model: Type[Warranty] = Warranty
    form_class: Type[WarrantyForm] = WarrantyForm
    template_name: str = "warranty/warranty_update.html"

    def form_valid(self, form) -> HttpResponse:
        product: str = form.cleaned_data.get('product_name')
        brand: str = form.cleaned_data.get('brand')
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

        try: 
            response = super().form_valid(form)
            messages.success(self.request, "Garantie modifiée avec succès.")
            return response
        except Exception:
            messages.error(self.request, f"Erreur lors de la modification de la garantie.")
            return self.form_invalid(form)

        
class WarrantyDeleteView(LoginRequiredMixin, UserWarrantyMixin, DeleteView):
    """Page Supprimer une garantie - confirmation avant de supprimer une garantie existante"""
    model: Type[Warranty] = Warranty
    template_name: str = 'warranty/warranties_list.html'
    context_object_name: str = "warranty"
    success_url: str = reverse_lazy("warranty:warranties_list")
   
    def form_valid(self, form) -> HttpResponse:
        product_name: str = self.object.product_name
        is_ajax: bool = self.request.headers.get('x-requested-with') == 'XMLHttpRequest'

        try: 
            self.object.delete()
            msg: str= f'Garantie "{product_name}" supprimée avec succès.'
            messages.success(self.request, msg)

            if is_ajax:
                message_html: str = render_to_string('partials/_messages.html', request=self.request)
                # vide la session pour éviter le doublon au refresh
                storage: messages.MessageStorage = messages.get_messages(self.request)
                storage.used = True

                return JsonResponse({
                    'status': 'success',
                    'message_html': message_html
                })
            return HttpResponseRedirect(self.get_success_url())

        except Exception:
            err_msg: str = f'Erreur lors de la suppression de la garantie "{product_name}".'
            messages.error(self.request, err_msg)

            if is_ajax:
                message_html: str = render_to_string('partials/_messages.html', request=self.request)
                storage: messages.MessageStorage = messages.get_messages(self.request)
                storage.used = True

                return JsonResponse({'status': 'error', 'message': err_msg}, status=400)    
            return super().form_invalid(form) 
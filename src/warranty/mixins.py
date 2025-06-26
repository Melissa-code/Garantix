from django.db.models import Q
from django.conf import settings
from datetime import datetime

class ContextDataMixin:
    """ Mixin pour afficher le context (media année courante user connecté total) """

    def get_context_data(self, **kwargs):
        # media 
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        # annee courante 
        annee_courante = datetime.now().year
        context['current_year'] = annee_courante
        # nom du user connecté
        if self.request.user.is_authenticated:
            context['nom_complet'] = f"{self.request.user.first_name} {self.request.user.last_name}".strip()
            context['nom_affichage'] = context['nom_complet'] if context['nom_complet'] else self.request.user.username
        # total officiers 
        if hasattr(self, 'model') and self.model: 
            context['total_warranties'] = self.model.objects.count()

        return context
    

class WarrantySearchMixin:
    """ Mixin pour rechercher une garnatie via un paramètre GET """

    search_param = "search"

    def get_queryset(self): 
        queryset = super().get_queryset()
        search_query = self.request.GET.get(self.search_param, "").strip()

        if search_query:
            queryset = queryset.filter(
                Q(product_name__icontains=search_query) |
                Q(brand__icontains=search_query) |
                Q(vendor__icontains=search_query) 
            )

        return queryset.order_by('product_name')
    

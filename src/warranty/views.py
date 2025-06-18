from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from warranty.models import Warranty
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.db.models import Q


class Home(TemplateView): 
    """ Page Accueil """
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context

@method_decorator(login_required, name="dispatch")
class WarrantiesList(ListView): 
    """ Page Liste de mes garanties """
    model = Warranty
    context_object_name = "warranties" # variable
    template_name = "warranty/warranties_list.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", "created_at", ]

@method_decorator(login_required, name="dispatch")
class WarrantyDetail(DetailView):
    """ Page Détail de la garantie """
    model = Warranty
    context_object_name = "warranty"
    template_name = "warranty/warranty_detail.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", "created_at", ]

@method_decorator(login_required, name="dispatch")
class WarrantyCreate(CreateView): 
    """ Page Créer une nouvelle garantie """
    model = Warranty
    template_name = "warranty/warranty_create.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", ]

@method_decorator(login_required, name="dispatch")
class WarrantyUpdate(UpdateView):
    """ Page Modifier une garantie """
    model = Warranty
    template_name = "warranty/warranty_update.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", ]

@method_decorator(login_required, name="dispatch")
class WarrantyDelete(DeleteView): 
    """ Page Supprimer une garantie """
    model = Warranty
    context_object_name = "warranty"
    success_url = reverse_lazy("warranty:home")
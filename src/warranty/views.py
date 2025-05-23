from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
from django.views.generic import ListView
from django.views.generic import CreateView
from warranty.models import Warranty
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View
from django.db.models import Q

# Page Accueil 
class Home(TemplateView): 
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context


# Page Liste des agents
@method_decorator(login_required, name="dispatch")
class WarrantiesList(ListView): 
    model = Warranty
    context_object_name = "warranties" # variable
    template_name = "warranty/warranties_list.html"
    fields = ["product_name", "brand", "purchase_date", "warranty_duration_months", "vendor", "imageReceipt", "notes", "created_at", ]

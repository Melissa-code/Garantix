from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings

# Page Accueil 
class Home(TemplateView): 
    template_name = "warranty/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_url'] = settings.MEDIA_URL
        return context

from django.urls import path
from django.contrib.auth import views as auth_views
from warranty.views import Home

# nom des urls 
app_name = 'warranty'

urlpatterns = [
  path('', Home.as_view(), name='home'), # page accueil 
  
]

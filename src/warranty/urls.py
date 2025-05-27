from django.urls import path
from django.contrib.auth import views as auth_views
from warranty.views import Home, WarrantiesList, WarrantyDetail

# nom des urls 
app_name = 'warranty'

urlpatterns = [
  path('', Home.as_view(), name='home'), # page accueil 
  path('warranties/', WarrantiesList.as_view(), name='warranties_list'), # page liste des garanties
  path('warranty/<int:pk>/', WarrantyDetail.as_view(), name='warranty_detail'),
  # page détail de la garantie
]

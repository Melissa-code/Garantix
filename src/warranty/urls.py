from django.urls import path
from django.contrib.auth import views as auth_views
from warranty.views import Home, WarrantiesList, WarrantyDetail, WarrantyCreate, WarrantyUpdate

# nom des urls 
app_name = 'warranty'

urlpatterns = [
  path('', Home.as_view(), name='home'), 
  path('warranties/', WarrantiesList.as_view(), name='warranties_list'),
  path('warranty/<int:pk>/', WarrantyDetail.as_view(), name='warranty_detail'), 
  path('create/', WarrantyCreate.as_view(), name='warranty_create'), 
  path('update/<int:pk>/', WarrantyUpdate.as_view(), name='warranty_update'), 
]

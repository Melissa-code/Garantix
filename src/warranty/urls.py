from django.urls import path
from django.contrib.auth import views as auth_views
from warranty.views import Home, WarrantiesList, WarrantyDetail, WarrantyCreate, WarrantyUpdate, WarrantyDelete

# nom des urls 
app_name = 'warranty'

urlpatterns = [
  path('', Home.as_view(), name='home'), 
  path('warranty/<int:pk>/', WarrantyDetail.as_view(), name='warranty_detail'), 
  path('update/<int:pk>/', WarrantyUpdate.as_view(), name='warranty_update'), 
  path('delete/<int:pk>/', WarrantyDelete.as_view(), name='warranty_delete'), 
  path('warranties/', WarrantiesList.as_view(), name='warranties_list'),
  path('create/', WarrantyCreate.as_view(), name='warranty_create'), 

]

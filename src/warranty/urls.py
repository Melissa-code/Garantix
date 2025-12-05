from django.urls import path
from django.contrib.auth import views as auth_views
from warranty import views
from django.conf import settings
from django.conf.urls.static import static


app_name = 'warranty'

urlpatterns = [
  path('', views.HomeView.as_view(), name='home'), 
  path('warranty/<int:pk>/', views.WarrantyDetailView.as_view(), name='warranty_detail'), 
  path('update/<int:pk>/', views.WarrantyUpdateView.as_view(), name='warranty_update'), 
  path('delete/<int:pk>/', views.WarrantyDeleteView.as_view(), name='warranty_delete'), 
  path('warranties/', views.WarrantiesListView.as_view(), name='warranties_list'),
  path('create/', views.WarrantyCreateView.as_view(), name='warranty_create'), 
]

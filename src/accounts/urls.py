from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.conf import settings
from django.conf.urls.static import static


# nom des urls 
app_name = 'accounts'

urlpatterns = [
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('signup/', views.SignupView.as_view(), name='signup'),
]

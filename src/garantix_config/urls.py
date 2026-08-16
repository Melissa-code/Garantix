from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve 
from garantix_config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('warranty.urls', namespace='warranty')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Sert les fichiers media (uploads des utilisateurs) en dev et en prod => trafic modéré par Nginx ou Apache en prod
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]


# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # images (photos de profil, uploads
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)  # CSS JS et icônes

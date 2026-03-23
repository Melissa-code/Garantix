from django.urls import reverse, resolve
from .base import WarrantyTestCase
from ..views import (
    HomeView, 
    WarrantiesListView, 
    WarrantyDeleteView,
    WarrantyDetailView, 
    WarrantyCreateView, 
    WarrantyUpdateView
  )


class WarrantyURLsTest(WarrantyTestCase):

    def test_home_url_resolves(self):
        """Vérifie que l'URL '/' appelle bien HomeView"""
        url = reverse('warranty:home')
        # resolve(url).func.view_class permet de retrouver la classe de la vue
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_list_url_resolves(self):
        """Vérifie l'URL de la liste"""
        url = reverse('warranty:warranties_list')
        self.assertEqual(resolve(url).func.view_class, WarrantiesListView)

    def test_detail_url_resolves(self):
        """Vérifie l'URL de détail (nécessite un PK)"""
        #PK de la garantie créée dans la classe mère
        url = reverse('warranty:warranty_detail', kwargs={'pk': self.warranty.pk})
        self.assertEqual(resolve(url).func.view_class, WarrantyDetailView)

    def test_create_url_resolves(self):
        """Vérifie l'URL de création"""
        url = reverse('warranty:warranty_create')
        self.assertEqual(resolve(url).func.view_class, WarrantyCreateView)

    def test_update_url_resolves(self):
        """Vérifie l'URL d'update"""
        url = reverse('warranty:warranty_update', kwargs={'pk': self.warranty.pk})
        self.assertEqual(resolve(url).func.view_class, WarrantyUpdateView)

    def test_delete_url_resolves(self):
        """Vérifie l'URL de suppression"""
        url = reverse('warranty:warranty_delete', kwargs={'pk': self.warranty.pk})
        self.assertEqual(resolve(url).func.view_class, WarrantyDeleteView)
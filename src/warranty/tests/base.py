from django.test import TestCase
from warranty.tests.factories import UserFactory, WarrantyFactory
from datetime import date
from django.utils import timezone


class WarrantyTestCase(TestCase):
    """Classe de base commune pour tous les tests Warranty"""
    
    def setUp(self):
        """classes filles héritent automatiquement de setup()"""

        self.user = UserFactory(username='testuser@example.com')
        self.warranty = WarrantyFactory(
            user=self.user,
            product_name="Produit_Test",
            brand="Marque_Test",
            purchase_date=date(2025, 12, 3), 
            warranty_duration_months=24,
            vendor="Revendeur_Test",
            notes="Observations_Test"
        )

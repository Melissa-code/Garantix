from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date, timedelta
from ..models import Warranty
from warranty.tests.base import WarrantyTestCase

class WarrantyModelTest(WarrantyTestCase):

    def test_warranty_creation(self):
        """Vérifie que la garantie de base créée dans la classe mère est correcte"""
        self.assertEqual(str(self.warranty), "Produit_Test (MARQUE_TEST)") # marque en MAJ comme dans le model (clean())
        self.assertEqual(self.warranty.user.username, "testuser@example.com")

    def test_warranty_expiry_calculation(self):
        """Vérifie le calcul via @property sur l'objet de la classe mère"""
        # purchase_date (2025-12-03) + (24 * 30 jours)
        expected_date = self.warranty.purchase_date + timedelta(days=self.warranty.warranty_duration_months * 30)
        self.assertEqual(self.warranty.warranty_expiry_date, expected_date)

    def test_unique_constraint_user_product_brand(self):
        """Vérifie l'unicité en utilisant l'objet existant comme premier exemplaire"""
        #doublon de self.warranty : même user, nom et marque
        duplicate = Warranty(
            user=self.user, 
            product_name=self.warranty.product_name, 
            brand=self.warranty.brand, 
            purchase_date=date(2026, 1, 1), 
            warranty_duration_months=6
        )
        with self.assertRaises(Exception): 
            duplicate.save()

    def test_purchase_date_cannot_be_in_future(self):
        """Vérifie que la validation clean() bloque les dates futures"""
        future_date = timezone.now().date() + timedelta(days=1)
        
        #nouvel objet (non sauvegardé) pour tester la validation
        invalid_warranty = Warranty(
            user=self.user,
            product_name="Futur-Phone",
            brand="Apple",
            purchase_date=future_date,
            warranty_duration_months=24
        )
        #lance une erreur 
        with self.assertRaises(ValidationError):
            invalid_warranty.full_clean()
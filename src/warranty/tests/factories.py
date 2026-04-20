import factory
from factory.django import DjangoModelFactory
from django.contrib.auth import get_user_model
from warranty.models import Warranty
from datetime import date

User = get_user_model()


class UserFactory(DjangoModelFactory):
    """Factory pour créer des utilisateurs de test"""
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f'user{n}@example.com')  # email comme username
    email = factory.LazyAttribute(lambda obj: obj.username) 
    password = factory.PostGenerationMethodCall('set_password', 'testpassword')


class WarrantyFactory(DjangoModelFactory):
    """Factory pour créer des garanties de test"""
    class Meta:
        model = Warranty
    
    user = factory.SubFactory(UserFactory)
    product_name = factory.Sequence(lambda n: f'Produit_{n}')
    brand = factory.Sequence(lambda n: f'Marque_{n}')
    purchase_date = date(2025, 12, 3)
    warranty_duration_months = 12
    vendor = "Revendeur Test"
    notes = "Notes de test"
    # imageReceipt : vide (null=True, blank=True)
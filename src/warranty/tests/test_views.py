from django.test import TestCase
from django.urls import reverse
from django.conf import settings 
from django.contrib.auth.models import User
from warranty.models import Warranty

class HomeViewTest(TestCase):

    def test_home_view_status_code(self):
        """Test HTTP status"""
        response = self.client.get(reverse('warranty:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_context(self): 
        """Test du rendu du template du contenu contextuel"""
        response = self.client.get(reverse('warranty:home'))
        self.assertIn('media_url', response.context)
        self.assertEqual(response.context['media_url'], settings.MEDIA_URL)


class test_warranties_list_view(TestCase):
    
    def setUp(self): 
        """
        Preparation des tests (ne commence pas par test)
        """
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        Warranty.objects.create(product_name="Produit_1", brand="Marque_1", purchase_date="2025-11-19", warranty_duration_months="12", vendor="Revendeur_1", imageReceipt="", notes="Observations_1", created_at="2025-11-19")
        Warranty.objects.create(product_name="Produit_2", brand="Marque_2", purchase_date="2025-11-20", warranty_duration_months="6", vendor="Revendeur_2", imageReceipt="", notes="Observations_2", created_at="2025-11-20")
        
    def test_warranties_created_in_setup(self):
        """
        Test si setUp a bien fonctionné
        """
        self.assertEqual(Warranty.objects.count(), 2)

    def test_redirect_if_not_logged(self): 
        """
        Test redirect to login
        """
        response = self.client.get(reverse('warranty:warranties_list'))
        self.assertEqual(response.status_code, 302)  

    def test_access_if_logged_in(self): 
        """
        Test accès à la liste (user autorisé)
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranties_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit_1")
        self.assertContains(response, "Produit_2")
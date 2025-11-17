from django.test import TestCase
from django.urls import reverse
from django.conf import settings 

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
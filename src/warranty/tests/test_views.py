from django.urls import reverse
from django.conf import settings 
from warranty.models import Warranty
from warranty.tests.factories import UserFactory
from warranty.tests.base import WarrantyTestCase
from datetime import date, timedelta
from django.utils import timezone

#---------------------------------- Warranty Home View Tests ----------------------------------#

class HomeViewTest(WarrantyTestCase):

    def test_home_view_status_code(self):
        """Test HTTP status"""
        response = self.client.get(reverse('warranty:home'))
        self.assertEqual(response.status_code, 200)

    def test_home_view_context(self): 
        """Test du rendu du template du contenu contextuel"""
        response = self.client.get(reverse('warranty:home'))
        self.assertIn('media_url', response.context)
        self.assertEqual(response.context['media_url'], settings.MEDIA_URL)


#---------------------------------- Warranty List View Tests ----------------------------------#

class WarrantyListViewTest(WarrantyTestCase):

    def test_redirect_if_not_logged(self): 
        """Test redirection vers connexion si pas connecté"""
        response = self.client.get(reverse('warranty:warranties_list'))
        self.assertEqual(response.status_code, 302)  

    def test_access_if_logged_in(self): 
        """Test accès à la liste (user autorisé)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranties_list'), {
            'product_name': f"Produit_Test",
            'brand': f"Marque_Test",
            'purchase_date': "2025-11-28",
            'warranty_duration_months': "24",
            'vendor': f"Revendeur_Test",
            'imageReceipt': "",
            'notes': f"Observations_Test",
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "Produit_Test")

    def test_user_cannot_access_other_user_warranty(self):
        """Un utilisateur ne peut pas voir les garanties d'un autre"""
        other_user = UserFactory(username="otheruser", password="otherpass123")
        self.client.force_login(other_user)
        url = reverse('warranty:warranties_list')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "Produit_Test")

    def test_user_sees_empty_list_when_no_warranties(self):
        """Test : un utilisateur sans garanties ne voit pas les garanties d'un autre et voit une liste vide"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranties_list'), {
            'product_name': f"Produit_Test",
            'brand': f"Marque_Test",
            'purchase_date': "2025-11-28",
            'warranty_duration_months': "24",
            'vendor': f"Revendeur_Test",
            'imageReceipt': "",
            'notes': f"Observations_Test",
        })
        # autre utilisateur sans garantie
        other_user = UserFactory(username="otheruser", password="otherpass123")
        self.client.force_login(other_user)

        url = reverse('warranty:warranties_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['warranties']), 0)
    

#---------------------------------- Warranty Detail View Tests ----------------------------------#

class WarrantyDetailViewTest(WarrantyTestCase):

    def test_redirect_if_not_logged(self):
        """Test redirection vers connexion si pas connecté"""
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302)

    def test_user_cannot_access_other_user_warranty(self):
        """Un utilisateur ne peut pas voir la garantie d'un autre"""
        other_user = UserFactory(username="otheruser", password="otherpass123")
        self.client.force_login(other_user)
        url = reverse('warranty:warranty_detail', args=[self.warranty.pk])  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_access_if_logged_in(self):
        """Test accès à la page profil (utilisateur autorisé)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit_Test")
        self.assertContains(response, "MARQUE_TEST")

    def test_warranty_not_found(self):
        """Test garantie non trouvée (ID inexistant)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_warranty_fields_in_context(self):
        """Test des champs de la garantie dans le contexte"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        warranty = response.context['warranty']
        self.assertEqual(warranty.product_name, "Produit_Test")
        self.assertEqual(warranty.brand, "MARQUE_TEST")
        self.assertEqual(str(warranty.purchase_date), "2025-12-03")
        self.assertEqual(warranty.warranty_duration_months, 24)
        self.assertEqual(warranty.vendor, "Revendeur_Test")
        self.assertEqual(warranty.notes, "Observations_Test")

    def test_warranty_imageReceipt_field(self):
        """Test du champ imageReceipt de la garantie"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        warranty = response.context['warranty']
        self.assertEqual(warranty.imageReceipt, "")


#---------------------------------- Warranty Create View Tests ----------------------------------#

class WarrantyCreateViewTest(WarrantyTestCase):

    def test_redirect_if_not_logged(self):
        """Test redirection vers connexion"""
        response = self.client.get(reverse('warranty:warranty_create'))
        self.assertEqual(response.status_code, 302)

    def test_access_if_logged_in(self):   
        """Test accès à la page de création (user authorized)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ajouter une garantie")

    def test_create_warranty(self):
        """Test création d'une nouvelle garantie"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_Nouveau",
            'brand': "MARQUE_NOUVEAU",
            'purchase_date': "2025-11-22",
            'warranty_duration_months': "18",
            'vendor': "Revendeur_Nouveau",
            'imageReceipt': "",
            'notes': "Observations_Nouveau",
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertEqual(Warranty.objects.count(), 2)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.product_name, "Produit_Nouveau")
        self.assertEqual(new_warranty.brand, "MARQUE_NOUVEAU")

    def test_warranties_created_in_setup(self):
        """Test si setUp a bien fonctionné: une garantie créée pour les tests"""
        self.assertEqual(Warranty.objects.count(), 1)  

    def test_create_warranty_missing_fields(self):
        """Test création de garantie avec des champs manquants (échouant sur les champs requis)"""
        self.client.force_login(self.user)
        initial_count = Warranty.objects.count()
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "",
            'brand': "MARQUE_INCOMPLETE",
            'purchase_date': "2025-11-23",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_Incomplete",
            'imageReceipt': "",
            'notes': "Observations_Incomplete",
        })
        self.assertEqual(response.status_code, 200)    # Reste sur même page 
        self.assertEqual(Warranty.objects.count(), initial_count)

    def test_create_warranty_invalid_date(self):
        """Test création de garantie avec une date d'achat invalide"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_InvalidDate",
            'brand': "MARQUE_INVALIDDATE",
            'purchase_date': "invalid-date",          # date invalide
            'warranty_duration_months': "12",
            'vendor': "Revendeur_InvalidDate",
            'imageReceipt': "",
            'notes': "Observations_InvalidDate",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Warranty.objects.count(), 1)  
    
    def test_create_warranty_negative_duration(self):
        """Test création de garantie avec une durée de garantie négative"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_NegativeDuration",
            'brand': "MARQUE_NEGATIVEDURATION",
            'purchase_date': "2025-11-24",
            'warranty_duration_months': "-5",          # durée négative
            'vendor': "Revendeur_NegativeDuration",
            'imageReceipt': "",
            'notes': "Observations_NegativeDuration",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Warranty.objects.count(), 1)  

    def test_create_warranty_optional_fields(self):
        """Test création de garantie avec des champs optionnels vides (imageReceipt et notes) ok"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_OptionalFields",
            'brand': "MARQUE_OPTIONALFIELDS",
            'purchase_date': "2025-11-25",
            'warranty_duration_months': "12",
            'vendor': "revendeur",
            'imageReceipt': "",
            'notes': "",
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 2)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.imageReceipt, "")
        self.assertEqual(new_warranty.notes, "")
    
    def test_create_warranty_long_notes(self):
        """Test création de garantie avec des notes très longues"""
        self.client.force_login(self.user)
        long_notes = "A" * 5000  
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_LongNotes",
            'brand': "MARQUE_LONGNOTES",
            'purchase_date': "2025-11-26",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_LongNotes",
            'imageReceipt': "",
            'notes': long_notes,
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 2)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.notes, long_notes)
    
    def test_create_warranty_special_characters(self):
        """Test création de garantie avec des caractères spéciaux dans les champs texte (ok pour les champs texte)"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_@#€%",
            'brand': "MARQUE_&*()",
            'purchase_date': "2025-11-27",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_!~",
            'imageReceipt': "",
            'notes': "Observations_<>?",
        })
        self.assertEqual(response.status_code, 200)  # reaffiche le formulaire avec erreurs de validation
        self.assertEqual(Warranty.objects.count(), 1) # setUp + 1 nouvelle mais elle est bloquée pas créée
        new_warranty = Warranty.objects.last()
        self.assertEqual(new_warranty.product_name, "Produit_Test")  # le champ product_name est requis et doit être valide donc la création échoue et la garantie créée est celle du setUp
        self.assertEqual(new_warranty.brand, "MARQUE_TEST")
        self.assertEqual(new_warranty.vendor, "Revendeur_Test")
        self.assertEqual(new_warranty.notes, "Observations_Test")
    
    def test_create_multiple_warranties(self):
        """Test création de plusieurs garanties successives"""
        self.client.force_login(self.user)
        for i in range(5):
            response = self.client.post(reverse('warranty:warranty_create'), {
                'product_name': f"Produit_{i}",
                'brand': f"MARQUE_{i}",
                'purchase_date': "2025-11-28",
                'warranty_duration_months': "12",
                'vendor': f"Revendeur_{i}",
                'imageReceipt': "",
                'notes': f"Observations_{i}",
            })
            self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 6)

    def test_create_warranty_whitespace_fields(self):
        """Test création de garantie avec des espaces dans les champs texte"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "   ",
            'brand': "   ",
            'purchase_date': "2025-11-29",
            'warranty_duration_months': "12",
            'vendor': "   ",
            'imageReceipt': "",
            'notes': "   ",
        })
        self.assertEqual(response.status_code, 200)  
        self.assertEqual(Warranty.objects.count(), 1)  # la création échoue à cause du champ product_name requis et valide, donc la garantie créée est celle du setUp


#---------------------------------- Warranty Update View Tests ----------------------------------#

class WarrantyUpdateViewTest(WarrantyTestCase):

    def test_redirect_if_not_logged(self):
        """Test redirect to login"""
        response = self.client.get(reverse('warranty:warranty_update', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 

    def test_access_if_logged_in(self):
        """Test access to update page (user authorized)"""
        self.client.force_login(self.user) 
        response = self.client.get(reverse('warranty:warranty_update', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modifier la garantie")   

    def test_update_warranty(self):
        """Test mise à jour d'une garantie existante avec des données valides"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_update', args=[self.warranty.id]), {
            'product_name': "Produit_Test",
            'brand': "MARQUE_TEST",
            'purchase_date': "2025-12-01",
            'warranty_duration_months': "24",
            'vendor': "Revendeur_Test",
            'imageReceipt': "",
            'notes': "Observations_Test",
        })
        self.assertEqual(response.status_code, 302) 
        self.warranty.refresh_from_db()
        self.assertEqual(self.warranty.product_name, "Produit_Test")
        self.assertEqual(self.warranty.brand, "MARQUE_TEST")
        self.assertEqual(str(self.warranty.purchase_date), "2025-12-01")
        self.assertEqual(self.warranty.warranty_duration_months, 24)
        self.assertEqual(self.warranty.vendor, "Revendeur_Test")
        self.assertEqual(self.warranty.notes, "Observations_Test")

    def test_update_warranty_invalid_data(self):
        """Test mise à jour avec des données invalides échouant sur les champs requis et les validations"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_update', args=[self.warranty.id]), {
            'product_name': "",
            'brand': "MARQUE_INVALIDE",
            'purchase_date': "invalid-date",
            'warranty_duration_months': "-10",
            'vendor': "Revendeur_Invalid",
            'imageReceipt': "",
            'notes': "Observations_Invalid",
        })
        self.assertEqual(response.status_code, 200)  
        self.warranty.refresh_from_db()
        self.assertEqual(self.warranty.product_name, "Produit_Test")
        self.assertEqual(self.warranty.brand, "MARQUE_TEST")
        self.assertEqual(str(self.warranty.purchase_date), "2025-12-03")
        self.assertEqual(self.warranty.warranty_duration_months, 24)       
        self.assertEqual(self.warranty.vendor, "Revendeur_Test")
        self.assertEqual(self.warranty.notes, "Observations_Test")       

    def test_update_warranty_partial_data(self):
        """Test mise à jour avec des données partielles échouant sur les champs requis"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_update', args=[self.warranty.id]), {
            'product_name': "Produit_PartialUpdate",
            'brand': "",
            'purchase_date': "2025-12-02",
            'warranty_duration_months': "18",
            'vendor': "",
            'imageReceipt': "",
            'notes': "",
        })
        self.assertEqual(response.status_code, 200)  
        self.warranty.refresh_from_db()
        self.assertEqual(self.warranty.product_name, "Produit_Test")
        self.assertEqual(self.warranty.brand, "MARQUE_TEST")
        self.assertEqual(str(self.warranty.purchase_date), "2025-12-03")
        self.assertEqual(self.warranty.warranty_duration_months, 24)       
        self.assertEqual(self.warranty.vendor, "Revendeur_Test")
        self.assertEqual(self.warranty.notes, "Observations_Test")   

    def test_update_warranty_different_user(self):
        """Test : un utilisateur ne peut pas modifier la garantie d'un autre"""
        other_user = UserFactory() 
        self.client.force_login(other_user)
        response = self.client.get(reverse('warranty:warranty_update', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 404)


#---------------------------------- Warranty Delete View Tests ----------------------------------#

class WarrantyDeleteViewTest(WarrantyTestCase):

    def test_redirect_if_not_logged(self):
        """Test redirect to login"""
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 

    def test_access_if_logged_in(self):
        """Test access to delete page (user authorized)"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
         
    def test_delete_warranty(self):
        """Test suppression d'une garantie existante"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 
        with self.assertRaises(Warranty.DoesNotExist):
            Warranty.objects.get(id=self.warranty.id)   

    def test_delete_nonexistent_warranty(self):
        """Test suppression d'une garantie inexistante"""
        self.client.force_login(self.user)
        response = self.client.post(reverse('warranty:warranty_delete', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_warranty_still_exists_after_cancel(self):
        """Test: la garantie existe toujours après une annulation de suppression"""
        self.client.force_login(self.user)
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        warranty_still_exists = Warranty.objects.filter(id=self.warranty.id).exists()
        self.assertTrue(warranty_still_exists)
    
    def test_delete_warranty_twice(self):
        """Test suppression de la même garantie deux fois pas possible"""
        self.client.force_login(self.user)
        response1 = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response1.status_code, 302) 
        response2 = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response2.status_code, 404)

    def test_delete_warranty_different_user(self):
        """Test qu'un utilisateur ne peut pas supprimer la garantie d'un autre"""
        other_user = UserFactory()  
        self.client.force_login(other_user)
        response = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 404)
        warranty_still_exists = Warranty.objects.filter(id=self.warranty.id).exists()
        self.assertTrue(warranty_still_exists)
        
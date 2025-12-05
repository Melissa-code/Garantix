from django.test import TestCase
from django.urls import reverse
from django.conf import settings 
from django.contrib.auth.models import User
from warranty.models import Warranty


####################################################################
### Home View Tests
####################################################################

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

####################################################################
### Warranty List View Tests
####################################################################

class WarrantyListViewTest(TestCase):
    
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

####################################################################
### Warranty Detail View Tests
####################################################################

class WarrantyDetailViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.warranty = Warranty.objects.create(
            product_name="Produit_Detail",
            brand="Marque_Detail",
            purchase_date="2025-11-21",
            warranty_duration_months="24",
            vendor="Revendeur_Detail",
            imageReceipt="",
            notes="Observations_Detail",
            created_at="2025-11-21"
        )

    def test_redirect_if_not_logged(self):
        """
        Test redirect to login
        """
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302)

    # def test_user_cannot_access_other_user_warranty(self):
    #     """Un utilisateur ne peut pas voir la garantie d'un autre"""
    #     other_user = User.objects.create_user(username='otheruser', password='otherpass123')
    #     self.client.login(username='otheruser', password='otherpass123')
    #     url = reverse('warranty:warranty_detail', args=[self.warranty.pk])  
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 404)

    def test_access_if_logged_in(self):
        """
        Test access to detail page (user authorized)
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Produit_Detail")
        self.assertContains(response, "Marque_Detail")

    def test_warranty_not_found(self):
        """
        Test for non-existing warranty
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_warranty_fields_in_context(self):
        """
        Test des champs de la garantie dans le contexte
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        warranty = response.context['warranty']
        self.assertEqual(warranty.product_name, "Produit_Detail")
        self.assertEqual(warranty.brand, "Marque_Detail")
        self.assertEqual(str(warranty.purchase_date), "2025-11-21")
        self.assertEqual(warranty.warranty_duration_months, 24)
        self.assertEqual(warranty.vendor, "Revendeur_Detail")
        self.assertEqual(warranty.notes, "Observations_Detail")
  
    def test_warranty_imageReceipt_field(self):
        """
        Test du champ imageReceipt de la garantie
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_detail', args=[self.warranty.id]))
        warranty = response.context['warranty']
        self.assertEqual(warranty.imageReceipt, "")

####################################################################
### Warranty Create View Tests
####################################################################

class WarrantyCreateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_redirect_if_not_logged(self):
        """
        Test redirect to login
        """
        response = self.client.get(reverse('warranty:warranty_create'))
        self.assertEqual(response.status_code, 302)

    def test_access_if_logged_in(self):
        """
        Test access to create page (user authorized)
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_create'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ajouter la garantie")

    def test_create_warranty(self):
        """
        Test création d'une nouvelle garantie
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_Nouveau",
            'brand': "Marque_Nouveau",
            'purchase_date': "2025-11-22",
            'warranty_duration_months': "18",
            'vendor': "Revendeur_Nouveau",
            'imageReceipt': "",
            'notes': "Observations_Nouveau",
        })
        self.assertEqual(response.status_code, 302)  # Redirection après création
        self.assertEqual(Warranty.objects.count(), 1)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.product_name, "Produit_Nouveau")
        self.assertEqual(new_warranty.brand, "Marque_Nouveau")

    def test_warranties_created_in_setup(self):
        """
        Test si setUp a bien fonctionné
        """
        self.assertEqual(Warranty.objects.count(), 0)  

    def test_create_warranty_missing_fields(self):
        """
        Test création de garantie avec des champs manquants
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "",
            'brand': "Marque_Incomplete",
            'purchase_date': "2025-11-23",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_Incomplete",
            'imageReceipt': "",
            'notes': "Observations_Incomplete",
        })
        self.assertEqual(response.status_code, 200)  # Reste sur même page 
        # self.assertFormError(response, 'form', 'product_name', 'This field is required.')
        self.assertEqual(Warranty.objects.count(), 0)  # Aucune garantie créée  

    def test_create_warranty_invalid_date(self):
        """
        Test création de garantie avec une date d'achat invalide
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_InvalidDate",
            'brand': "Marque_InvalidDate",
            'purchase_date': "invalid-date",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_InvalidDate",
            'imageReceipt': "",
            'notes': "Observations_InvalidDate",
        })
        self.assertEqual(response.status_code, 200)  
        # self.assertFormError(response, 'form', 'purchase_date', 'Enter a valid date.')
        self.assertEqual(Warranty.objects.count(), 0)  
    
    def test_create_warranty_negative_duration(self):
        """
        Test création de garantie avec une durée de garantie négative
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_NegativeDuration",
            'brand': "Marque_NegativeDuration",
            'purchase_date': "2025-11-24",
            'warranty_duration_months': "-5",
            'vendor': "Revendeur_NegativeDuration",
            'imageReceipt': "",
            'notes': "Observations_NegativeDuration",
        })
        self.assertEqual(response.status_code, 200)  
        # self.assertFormError(response, 'form', 'warranty_duration_months', 'Ensure this value is greater than or equal to 0.')
        self.assertEqual(Warranty.objects.count(), 0)  

    def test_create_warranty_optional_fields(self):
        """
        Test création de garantie avec des champs optionnels vides
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_OptionalFields",
            'brand': "Marque_OptionalFields",
            'purchase_date': "2025-11-25",
            'warranty_duration_months': "12",
            'vendor': "revendeur",
            'imageReceipt': "",
            'notes': "",
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 1)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.imageReceipt, "")
        self.assertEqual(new_warranty.notes, "")
    
    def test_create_warranty_long_notes(self):
        """
        Test création de garantie avec des notes très longues
        """
        self.client.login(username="testuser", password="testpassword")
        long_notes = "A" * 5000  
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_LongNotes",
            'brand': "Marque_LongNotes",
            'purchase_date': "2025-11-26",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_LongNotes",
            'imageReceipt': "",
            'notes': long_notes,
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 1)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.notes, long_notes)
    
    def test_create_warranty_special_characters(self):
        """
        Test création de garantie avec des caractères spéciaux dans les champs texte
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_create'), {
            'product_name': "Produit_@#€%",
            'brand': "Marque_&*()",
            'purchase_date': "2025-11-27",
            'warranty_duration_months': "12",
            'vendor': "Revendeur_!~",
            'imageReceipt': "",
            'notes': "Observations_<>?",
        })
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 1)
        new_warranty = Warranty.objects.first()
        self.assertEqual(new_warranty.product_name, "Produit_@#€%")
        self.assertEqual(new_warranty.brand, "Marque_&*()")
        self.assertEqual(new_warranty.vendor, "Revendeur_!~")
        self.assertEqual(new_warranty.notes, "Observations_<>?")
    
    def test_create_multiple_warranties(self):
        """
        Test création de plusieurs garanties successives
        """
        self.client.login(username="testuser", password="testpassword")
        for i in range(5):
            response = self.client.post(reverse('warranty:warranty_create'), {
                'product_name': f"Produit_{i}",
                'brand': f"Marque_{i}",
                'purchase_date': "2025-11-28",
                'warranty_duration_months': "12",
                'vendor': f"Revendeur_{i}",
                'imageReceipt': "",
                'notes': f"Observations_{i}",
            })
            self.assertEqual(response.status_code, 302)  
        self.assertEqual(Warranty.objects.count(), 5)

    def test_create_warranty_whitespace_fields(self):
        """
        Test création de garantie avec des espaces dans les champs texte
        """
        self.client.login(username="testuser", password="testpassword")
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
        self.assertEqual(Warranty.objects.count(), 0)

####################################################################
### Warranty Update View Tests  
####################################################################

class WarrantyUpdateViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.warranty = Warranty.objects.create(
            product_name="Produit_Update",
            brand="Marque_Update",
            purchase_date="2025-11-30",
            warranty_duration_months="12",
            vendor="Revendeur_Update",
            imageReceipt="",
            notes="Observations_Update",
            created_at="2025-11-30"
        )   

    def test_redirect_if_not_logged(self):
        """ Test redirect to login 
        """
        response = self.client.get(reverse('warranty:warranty_update', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 

    def test_access_if_logged_in(self):
        """ Test access to update page (user authorized) 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_update', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Modifier la garantie")   

    def test_update_warranty(self):
        """ Test mise à jour d'une garantie existante 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_update', args=[self.warranty.id]), {
            'product_name': "Produit_Updated",
            'brand': "Marque_Updated",
            'purchase_date': "2025-12-01",
            'warranty_duration_months': "24",
            'vendor': "Revendeur_Updated",
            'imageReceipt': "",
            'notes': "Observations_Updated",
        })
        self.assertEqual(response.status_code, 302) 
        updated_warranty = Warranty.objects.get(id=self.warranty.id)
        self.assertEqual(updated_warranty.product_name, "Produit_Updated")
        self.assertEqual(updated_warranty.brand, "Marque_Updated")
        self.assertEqual(str(updated_warranty.purchase_date), "2025-12-01")
        self.assertEqual(updated_warranty.warranty_duration_months, 24)
        self.assertEqual(updated_warranty.vendor, "Revendeur_Updated")
        self.assertEqual(updated_warranty.notes, "Observations_Updated")
    
    def test_update_warranty_invalid_data(self):
        """ Test mise à jour avec des données invalides 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_update', args=[self.warranty.id]), {
            'product_name': "",
            'brand': "Marque_Invalid",
            'purchase_date': "invalid-date",
            'warranty_duration_months': "-10",
            'vendor': "Revendeur_Invalid",
            'imageReceipt': "",
            'notes': "Observations_Invalid",
        })
        self.assertEqual(response.status_code, 200)  
        warranty_after_attempt = Warranty.objects.get(id=self.warranty.id)
        self.assertEqual(warranty_after_attempt.product_name, "Produit_Update")
        self.assertEqual(warranty_after_attempt.brand, "Marque_Update")
        self.assertEqual(str(warranty_after_attempt.purchase_date), "2025-11-30")
        self.assertEqual(warranty_after_attempt.warranty_duration_months, 12)       
        self.assertEqual(warranty_after_attempt.vendor, "Revendeur_Update")
        self.assertEqual(warranty_after_attempt.notes, "Observations_Update")       

    def test_update_warranty_partial_data(self):
        """ Test mise à jour avec des données partielles 
        """
        self.client.login(username="testuser", password="testpassword")
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
        warranty_after_attempt = Warranty.objects.get(id=self.warranty.id)
        self.assertEqual(warranty_after_attempt.product_name, "Produit_Update")
        self.assertEqual(warranty_after_attempt.brand, "Marque_Update")
        self.assertEqual(str(warranty_after_attempt.purchase_date), "2025-11-30")
        self.assertEqual(warranty_after_attempt.warranty_duration_months, 12)       
        self.assertEqual(warranty_after_attempt.vendor, "Revendeur_Update")
        self.assertEqual(warranty_after_attempt.notes, "Observations_Update")   

####################################################################
### Warranty Delete View Tests  
####################################################################

class WarrantyDeleteViewTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.warranty = Warranty.objects.create(
            product_name="Produit_Delete",
            brand="Marque_Delete",
            purchase_date="2025-12-03",
            warranty_duration_months="12",
            vendor="Revendeur_Delete",
            imageReceipt="",
            notes="Observations_Delete",
            created_at="2025-12-03"
        )   

    def test_redirect_if_not_logged(self):
        """ Test redirect to login 
        """
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 

    def test_access_if_logged_in(self):
        """ Test access to delete page (user authorized) 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
         
    def test_delete_warranty(self):
        """ Test suppression d'une garantie existante 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 302) 
        with self.assertRaises(Warranty.DoesNotExist):
            Warranty.objects.get(id=self.warranty.id)   

    def test_delete_nonexistent_warranty(self):
        """ Test suppression d'une garantie inexistante 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(reverse('warranty:warranty_delete', args=[999]))
        self.assertEqual(response.status_code, 404)
    
    def test_warranty_still_exists_after_cancel(self):
        """ Test que la garantie existe toujours après une annulation de suppression 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)
        warranty_still_exists = Warranty.objects.filter(id=self.warranty.id).exists()
        self.assertTrue(warranty_still_exists)
    
    def test_delete_warranty_twice(self):
        """ Test suppression de la même garantie deux fois 
        """
        self.client.login(username="testuser", password="testpassword")
        response1 = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response1.status_code, 302) 
        response2 = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response2.status_code, 404)
    
    def test_delete_warranty_invalid_method(self):
        """ Test suppression avec une méthode HTTP invalide 
        """
        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
        self.assertEqual(response.status_code, 200)  
        warranty_still_exists = Warranty.objects.filter(id=self.warranty.id).exists()
        self.assertTrue(warranty_still_exists)

    # def test_delete_warranty_different_user(self):
    #     """ Test qu'un utilisateur ne peut pas supprimer la garantie d'un autre 
    #     """
    #     other_user = User.objects.create_user(username='otheruser', password='otherpass123')
    #     self.client.login(username='otheruser', password='otherpass123')
    #     response = self.client.post(reverse('warranty:warranty_delete', args=[self.warranty.id]))
    #     self.assertEqual(response.status_code, 404)
    #     warranty_still_exists = Warranty.objects.filter(id=self.warranty.id).exists()
    #     self.assertTrue(warranty_still_exists)

    # def test_delete_warranty_confirmation_page(self):
    #     """ Test de la page de confirmation de suppression 
    #     """
    #     self.client.login(username="testuser", password="testpassword")
    #     response = self.client.get(reverse('warranty:warranty_delete', args=[self.warranty.id]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, f"Etes-vous sûr de vouloir supprimer la garantie {self.warranty.product_name} ?")

    
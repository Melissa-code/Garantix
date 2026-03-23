from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta


class Warranty(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warranties', verbose_name="Utilisateur", null=True, blank=True)
    product_name = models.CharField(max_length=200, verbose_name="Nom du produit")
    brand = models.CharField(max_length=150, verbose_name="Nom de la marque")
    purchase_date = models.DateField(verbose_name="Date d'achat")
    warranty_duration_months = models.PositiveIntegerField(verbose_name="Durée de garantie (en mois)")
    vendor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fournisseur")
    imageReceipt = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name="Image du reçu")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Crée le")

    class Meta:
        """return les résultats triés par ordre alphabétique du nom puis par marque si même nom"""
        ordering = ['product_name', 'brand'] # tri par nom d'abord puis par marque si même nom 
        verbose_name = "Garanties"

    def get_absolute_url(self):
        """redirection après ajout/modification d'une garantie vers la liste des garanties"""

        return reverse('warranty:warranties_list') 
    
    @property
    def warranty_expiry_date(self): 
        """calcule la date d'expiration de la garantie en ajoutant la durée de garantie à la date d'achat"""
        return self.purchase_date + timedelta(days=self.warranty_duration_months * 30)
    
    def __str__(self):
        """method to string"""
        return f"{self.product_name} {self.brand}"

from django.db import models
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import timedelta, timezone
from django.utils import timezone


class Warranty(models.Model): 
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='warranties', verbose_name="Utilisateur")
    product_name = models.CharField(max_length=150, verbose_name="Nom du produit")
    brand = models.CharField(max_length=150, validators=[MinLengthValidator(2)], verbose_name="Nom de la marque")
    purchase_date = models.DateField(verbose_name="Date d'achat")
    warranty_duration_months = models.PositiveIntegerField(verbose_name="Durée de garantie (en mois)")
    vendor = models.CharField(max_length=100, blank=True, null=True, verbose_name="Fournisseur")
    imageReceipt = models.ImageField(upload_to='receipts/', blank=True, null=True, verbose_name="Image du reçu")
    notes = models.TextField(blank=True, null=True, verbose_name="Notes")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Crée le")

    class Meta:
        """return les résultats triés par ordre alphabétique du nom puis par marque si même nom"""
        ordering = ['product_name', 'brand'] 
        verbose_name = "Garantie"
        verbose_name_plural = "Garanties"
        # utilisateur ne peut pas créer deux fois le même produit/marque
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'product_name', 'brand'], 
                name='unique_user_warranty'
            )
        ]
    
    def clean(self):
        """Validations personnalisées pour les champs de la garantie"""
        super().clean()
        # date d'achat ne peut pas etre dans le futur
        if self.purchase_date and self.purchase_date > timezone.now().date():
            raise ValidationError({
                'purchase_date': "La date d'achat ne peut pas être dans le futur."
            })
        
        # durée de garantie doit etre realiste (max 20 ans)
        if self.warranty_duration_months and self.warranty_duration_months > 240:
            raise ValidationError({
                'warranty_duration_months': "La durée de garantie est trop élevée. Veuillez entrer une durée réaliste."
            })
        

    def save(self, *args, **kwargs):
        """execution de clean() avant de sauvegarder"""
        self.full_clean()
        super().save(*args, **kwargs)


    def get_absolute_url(self):
        """redirection après ajout/modification d'une garantie vers la liste des garanties"""
        return reverse('warranty:warranties_list') 
    

    @property
    def warranty_expiry_date(self): 
        """calcule la date d'expiration approximative de la garantie en ajoutant la durée de garantie à la date d'achat
        -> Python transforme cette fonction en attribut "virtuel"""
        return self.purchase_date + timedelta(days=self.warranty_duration_months * 30)
    
    
    @property
    def is_active(self):
        """Vérifie si la garantie est toujours valide à la date d'aujourd'hui"""
        return self.warranty_expiry_date >= timezone.now().date()


    def __str__(self):
        """methode d'affichage d'une garantie dans l'admin et les listes - affiche le nom du produit et la marque"""
        return f"{self.product_name} ({self.brand})"

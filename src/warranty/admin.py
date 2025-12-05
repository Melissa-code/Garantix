from django.contrib import admin
from warranty.models import Warranty


class WarrantyAdmin(admin.ModelAdmin): 
    list_display = (
        "product_name", 
        "brand", 
        "purchase_date",
        "warranty_duration_months", 
        "vendor", 
        "imageReceipt", 
        "notes", 
        "created_at",
    )
    # editer certains champs dans l'interface admin 
    list_editable = (
       #
    )

# relie le modele Warranty à la classe Admin
admin.site.register(Warranty, WarrantyAdmin)
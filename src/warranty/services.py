from warranty.models import Warranty
from django.db.models import QuerySet

def get_user_warranties(user) -> QuerySet[Warranty]:
  """Récupère les garanties par ordre alphabétique associées à un utilisateur donné sinon [vide]"""
  return Warranty.objects.filter(user=user).order_by('product_name')

from warranty.models import Warranty

def get_user_warranties(user):
  """Récupère les garanties par ordre alphabétique associées à un utilisateur donné"""
  return Warranty.objects.filter(user=user).order_by('product_name')

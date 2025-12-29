from .models import Favoritos

def favoritos_total_items(request):
    if not request.user.is_authenticated:
        return 0

    favoritos = Favoritos.objects.filter(usuario=request.user).first()
    if not favoritos:
        return 0

    return favoritos.items.count()

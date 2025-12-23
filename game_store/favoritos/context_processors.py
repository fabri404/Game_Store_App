from .models import Favoritos

def favoritos_total_items(request):
    if not request.user.is_authenticated:
        return {"favoritos_total_items": 0}

    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    return {"favoritos_total_items": favoritos.items.count()}

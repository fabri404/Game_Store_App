from .models import Carrito

def carrito_total_items(request):
    if not request.user.is_authenticated:
        return 0

    carrito = Carrito.objects.filter(usuario=request.user).first()
    if not carrito:
        return 0

    return sum(item.cantidad for item in carrito.items.all())

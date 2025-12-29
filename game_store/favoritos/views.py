from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from catalogo.models import Juego
from .models import Favoritos, ItemFavorito

from carrito.utils import carrito_total_items
from favoritos.utils import favoritos_total_items


@login_required
def agregar_favorito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)

    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)

    # evitar duplicados
    ItemFavorito.objects.get_or_create(
        favoritos=favoritos,
        juego=juego
    )

    # 👉 AJAX: actualizar header sin recargar
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "carrito": carrito_total_items(request),
            "favoritos": favoritos_total_items(request),
        })

    # 👉 flujo normal
    return redirect("favoritos:ver_favoritos")


@login_required
def ver_favoritos(request):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    items = favoritos.items.select_related("juego")

    return render(
        request,
        "favoritos/ver_favoritos.html",
        {
            "favoritos": favoritos,
            "items": items,
        }
    )


@login_required
def eliminar_favorito(request, juego_id):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    item = favoritos.items.filter(juego_id=juego_id).first()
    if item:
        item.delete()
    return redirect("favoritos:ver_favoritos")

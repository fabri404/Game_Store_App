from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from catalogo.models import Juego
from .models import Favoritos, ItemFavorito
from django.http import JsonResponse


@login_required
def agregar_favorito(request, juego_id):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    juego = get_object_or_404(Juego, id=juego_id)

    ItemFavorito.objects.get_or_create(favoritos=favoritos, juego=juego)

    # Si viene por AJAX (fetch), NO redirigir: devolvemos OK y no se mueve el scroll
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"ok": True})

    next_url = request.GET.get("next") or request.POST.get("next") or request.META.get("HTTP_REFERER")
    return redirect(next_url or "favoritos:ver_favoritos")

@login_required
def ver_favoritos(request):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    items = favoritos.items.select_related("juego")
    return render(request, "favoritos/ver_favoritos.html", {"favoritos": favoritos, "items": items})


@login_required
def eliminar_favorito(request, juego_id):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    item = favoritos.items.filter(juego_id=juego_id).first()
    if item:
        item.delete()
    return redirect("favoritos:ver_favoritos")

@login_required
def agregar_favorito(request, juego_id):
    favoritos, _ = Favoritos.objects.get_or_create(usuario=request.user)
    juego = get_object_or_404(Juego, id=juego_id)
    ItemFavorito.objects.get_or_create(favoritos=favoritos, juego=juego)
    return redirect(request.META.get("HTTP_REFERER", "favoritos:ver_favoritos"))

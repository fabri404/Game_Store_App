from django.shortcuts import render
from django.core.paginator import Paginator
from django.db.models import Q

from .models import Juego

PLATFORM_CATEGORIES = ["PC", "PS5", "PS4", "Xbox Series X", "Switch"]  # tus 5 categorías


def _filter_by_platform_token(qs, token: str):
    # Match por token completo dentro de "PC, PS5, ..."
    return qs.filter(
        Q(plataforma=token) |
        Q(plataforma__startswith=f"{token}, ") |
        Q(plataforma__endswith=f", {token}") |
        Q(plataforma__contains=f", {token}, ")
    )


def lista_juegos(request):
    qs = Juego.objects.all().order_by("id")

    q = (request.GET.get("q") or "").strip()
    plat = (request.GET.get("plat") or "").strip()
    order = (request.GET.get("order") or "").strip()

    if q:
        qs = qs.filter(Q(nombre__icontains=q) | Q(plataforma__icontains=q))

    if plat in PLATFORM_CATEGORIES:
        qs = _filter_by_platform_token(qs, plat)

    if order in ("precio", "-precio", "nombre", "-nombre", "id", "-id"):
        qs = qs.order_by(order)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "lista_juegos": page_obj,
        "q": q,
        "plat": plat,
        "order": order,
        "platform_categories": PLATFORM_CATEGORIES,
    }
    return render(request, "catalogo/lista_juegos.html", context)

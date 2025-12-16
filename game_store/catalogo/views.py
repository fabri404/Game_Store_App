from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Juego

def lista_juegos(request):
    qs = Juego.objects.all().order_by("id")

    q = request.GET.get("q", "").strip()
    plataforma = request.GET.get("plataforma", "").strip()
    precio_min = request.GET.get("min", "").strip()
    precio_max = request.GET.get("max", "").strip()
    order = request.GET.get("order", "").strip()

    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(plataforma__icontains=q)
        )

    if plataforma:
        qs = qs.filter(plataforma__icontains=plataforma)

    if precio_min:
        try:
            qs = qs.filter(precio__gte=float(precio_min))
        except ValueError:
            pass

    if precio_max:
        try:
            qs = qs.filter(precio__lte=float(precio_max))
        except ValueError:
            pass

    if order in ("precio", "-precio", "nombre", "-nombre", "id", "-id"):
        qs = qs.order_by(order)

    paginator = Paginator(qs, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    contexto = {
        "lista_juegos": page_obj,
        "q": q,
        "plataforma": plataforma,
        "precio_min": precio_min,
        "precio_max": precio_max,
        "order": order,
    }
    return render(request, "catalogo/lista_juegos.html", contexto)

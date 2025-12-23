from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Carrito, Itemcarrito
from catalogo.models import Juego   

@login_required
def agregar_al_carrito(request, juego_id):
    juego = get_object_or_404(Juego, id=juego_id)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)

    itemcarrito, creado = Itemcarrito.objects.get_or_create(carrito=carrito, juego=juego)

    if not creado:
        itemcarrito.cantidad += 1
    itemcarrito.save()

    return redirect('catalogo:detalle_juego', pk=juego_id)

@login_required
def ver_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    items = carrito.items.select_related('juego')
    total_precio = carrito.total_precio()
    return render(request, 'carrito/ver_carrito.html', {'carrito': carrito, 
                                                        'items': items, 'total_precio': total_precio})


@login_required
def eliminar_del_carrito(request, juego_id):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    itemcarrito = carrito.items.filter(juego_id=juego_id).first()
    if itemcarrito:
        itemcarrito.delete()
    return redirect('carrito:ver_carrito')


@login_required
def limpiar_carrito(request):
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    carrito.items.all().delete()
    return redirect('carrito:ver_carrito')

     
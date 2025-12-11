from django.shortcuts import render
from .models import Juego
from django.core.paginator import Paginator


def lista_juegos(request):
    juegos = Juego.objects.all().order_by('id')

    paginator = Paginator(juegos, 6)  # Mostrar 6 juegos por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)  


    contexto_catalogo_juegos = {'lista_juegos': page_obj}
    return render(request, 'catalogo/lista_juegos.html', contexto_catalogo_juegos)

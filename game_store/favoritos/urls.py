from django.urls import path
from . import views 

app_name = 'favoritos'

urlpatterns = [
    path("", views.ver_favoritos, name="ver_favoritos"),
    path("eliminar/<int:juego_id>/", views.eliminar_favorito, name="eliminar_favorito"),
    path("agregar/<int:juego_id>/", views.agregar_favorito, name="agregar_favorito"),

]
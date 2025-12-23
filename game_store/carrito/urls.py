from django.urls import path
from . import views 

app_name = 'carrito'    

urlpatterns = [
    path('',views.ver_carrito, name='ver_carrito'),
    path('agregar/<int:juego_id>/', views.agregar_al_carrito,
         name='agregar_al_carrito'),
    path('eliminar/<int:juego_id>/', views.eliminar_del_carrito,
        name='eliminar_del_carrito'),
    path('limpiar/', views.limpiar_carrito, name='limpiar_carrito'),
    path("incrementar/<int:juego_id>/", views.incrementar_cantidad, name="incrementar_cantidad"),
    path("decrementar/<int:juego_id>/", views.decrementar_cantidad, name="decrementar_cantidad"),

]
from django.urls import path
from . import views 
urlpatterns = [
    path('', views.lista_juegos, name='lista_juegos'),
    path('<int:pk>/', views.detalle_juego, name='detalle_juego'),
]
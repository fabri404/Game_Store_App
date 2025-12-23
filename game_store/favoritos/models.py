# favoritos/models.py
from django.db import models
from django.conf import settings
from catalogo.models import Juego


class Favoritos(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favoritos"
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Favoritos de {self.usuario}"


class ItemFavorito(models.Model):
    favoritos = models.ForeignKey(
        Favoritos,             
        on_delete=models.CASCADE,
        related_name="items"
    )
    juego = models.ForeignKey(Juego, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("favoritos", "juego")

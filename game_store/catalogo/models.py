from django.db import models

class Juego(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    plataforma = models.CharField(max_length=80)

    def __str__(self):
        return self.nombre

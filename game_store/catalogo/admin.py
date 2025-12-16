from django.contrib import admin
from .models import Juego   

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "plataforma")
    search_fields = ("nombre", "plataforma")
    list_filter = ("plataforma",)
    ordering = ("id",)
    list_per_page = 25

    def precio_2d(self, obj):
        return f"{obj.precio:.2f}"
    precio_2d.short_description = "Precio"
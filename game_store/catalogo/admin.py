from django.contrib import admin
from django.db.models import Q
from .models import Juego

# Definí acá tus categorías
PLATFORM_FILTER_CHOICES = [
    "PC",
    "PS5",
    "PS4",
    "PS3",
    "PS2",
    "Xbox Series X",
    "Xbox Series S",
    "Switch",
    "Switch Oled",
    "Switch 2",
]

class PlataformaTokenFilter(admin.SimpleListFilter):
    title = "Plataforma (categorías)"
    parameter_name = "plat"

    def lookups(self, request, model_admin):
        return [(p, p) for p in PLATFORM_FILTER_CHOICES]

    def queryset(self, request, queryset):
        token = self.value()
        if not token:
            return queryset

        # Match por token completo usando el formato normalizado ", "
        return queryset.filter(
            Q(plataforma=token) |
            Q(plataforma__startswith=f"{token}, ") |
            Q(plataforma__endswith=f", {token}") |
            Q(plataforma__contains=f", {token}, ")
        )

@admin.register(Juego)
class JuegoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "precio", "plataforma")
    search_fields = ("nombre", "plataforma")
    list_filter = (PlataformaTokenFilter,)  # <- clave: ya no filtra por combinación
    ordering = ("id",)

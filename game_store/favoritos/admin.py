from django.contrib import admin
from .models import Favoritos, ItemFavorito


class ItemFavoritoInline(admin.TabularInline):
    model = ItemFavorito
    extra = 0
    can_delete = True

    # Recomendado si tenés muchos juegos (requiere search_fields en JuegoAdmin)
    autocomplete_fields = ["juego"]

    fields = (
        "juego",
        "juego_plataforma",
        "juego_precio",
        "creado",
    )
    readonly_fields = (
        "juego_plataforma",
        "juego_precio",
        "creado",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("juego")

    @admin.display(description="Plataforma")
    def juego_plataforma(self, obj):
        return getattr(obj.juego, "plataforma", "-")

    @admin.display(description="Precio")
    def juego_precio(self, obj):
        return getattr(obj.juego, "precio", "-")


@admin.register(Favoritos)
class FavoritosAdmin(admin.ModelAdmin):
    inlines = [ItemFavoritoInline]

    list_display = ("id", "usuario", "total_items_admin", "creado", "actualizado")
    search_fields = ("usuario__username", "usuario__email")
    list_filter = ("creado", "actualizado")
    date_hierarchy = "creado"
    ordering = ("-actualizado",)
    readonly_fields = ("creado", "actualizado")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("usuario").prefetch_related("items__juego")

    @admin.display(description="Items")
    def total_items_admin(self, obj):
        return obj.items.count()


@admin.register(ItemFavorito)
class ItemFavoritoAdmin(admin.ModelAdmin):
    """
    Vista plana para métricas:
    - qué juegos son más guardados
    - por quién
    - cuándo
    """
    list_display = ("id", "usuario", "juego", "plataforma", "precio", "creado")
    search_fields = (
        "favoritos__usuario__username",
        "favoritos__usuario__email",
        "juego__nombre",
    )
    list_filter = ("creado", "juego")
    date_hierarchy = "creado"
    ordering = ("-creado",)

    autocomplete_fields = ["favoritos", "juego"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related("favoritos__usuario", "juego")

    @admin.display(description="Usuario")
    def usuario(self, obj):
        return obj.favoritos.usuario

    @admin.display(description="Plataforma")
    def plataforma(self, obj):
        return getattr(obj.juego, "plataforma", "-")

    @admin.display(description="Precio")
    def precio(self, obj):
        return getattr(obj.juego, "precio", "-")

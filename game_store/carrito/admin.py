from django.contrib import admin
from.models import Carrito, Itemcarrito 

class ItemCarritoInline(admin.TabularInline):
    model = Itemcarrito
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Carrito)
class CarritoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'creado', 'actualizado', 'total_items', 'total_precio')
    search_fields = ('usuario__username',)
    inlines = [ItemCarritoInline]
    

@admin.register(Itemcarrito)    
class ItemCarritoAdmin(admin.ModelAdmin):
    list_display = ('carrito', 'juego', 'cantidad', 'subtotal')
    list_filter = ('carrito', 'juego')
    search_fields = ('juego__nombre', 'carrito__usuario__username')
    readonly_fields=('subtotal',)



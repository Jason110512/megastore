from django.contrib import admin
from .models import Producto, Categoria, Orden, OrdenItem, Carrito, CarritoItem, Factura
admin.site.register([Producto, Categoria, Orden, OrdenItem, Carrito, CarritoItem, Factura])

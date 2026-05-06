from django.urls import path
from . import views

urlpatterns = [
    # Cliente
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:pk>/', views.detalle_producto, name='detalle_producto'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
    path('carrito/quitar/<int:producto_id>/', views.quitar_carrito, name='quitar_carrito'),
    path('carrito/eliminar/<int:producto_id>/', views.eliminar_item_carrito, name='eliminar_item_carrito'),
    path('envio/', views.envio, name='envio'),
    path('mis-ordenes/', views.mis_ordenes, name='mis_ordenes'),
    path('mis-facturas/', views.mis_facturas, name='mis_facturas'),
    path('ubicaciones/', views.ubicaciones, name='ubicaciones'),

    # Admin
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/productos/', views.admin_productos, name='admin_productos'),
    path('admin/productos/registrar/', views.registrar_producto, name='registrar_producto'),
    path('admin/productos/<int:pk>/actualizar/', views.actualizar_producto, name='actualizar_producto'),
    path('admin/productos/<int:pk>/eliminar/', views.eliminar_producto, name='eliminar_producto'),
    path('admin/pedidos/', views.admin_pedidos, name='admin_pedidos'),
    path('admin/pedidos/<int:pk>/aprobar/', views.aprobar_orden, name='aprobar_orden'),
    path('admin/pedidos/<int:pk>/eliminar/', views.eliminar_orden, name='eliminar_orden'),
]

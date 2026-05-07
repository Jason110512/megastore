from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum
from django.http import JsonResponse
from django.core.paginator import Paginator
from .models import Producto, Categoria, Carrito, CarritoItem, Orden, OrdenItem, Factura
from .forms import ProductoForm, EnvioForm
from .decorators import admin_required
from accounts.models import Usuario


def catalogo(request):
    query = request.GET.get('q', '')
    categoria_id = request.GET.get('categoria', '')
    productos = Producto.objects.filter(disponible=True).order_by('-fecha_creacion')

    if query:
        productos = productos.filter(Q(nombre__icontains=query) | Q(descripcion__icontains=query))
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    paginator = Paginator(productos, 10)
    page = request.GET.get('page', 1)
    productos_page = paginator.get_page(page)
    categorias = Categoria.objects.all()

    carrito_items = {}
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            for item in carrito.items.all():
                carrito_items[item.producto_id] = item.cantidad
        except Carrito.DoesNotExist:
            pass

    return render(request, 'store/catalogo.html', {
        'productos': productos_page,
        'categorias': categorias,
        'query': query,
        'carrito_items': carrito_items,
    })


def detalle_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk, disponible=True)
    productos_relacionados = Producto.objects.filter(
        categoria=producto.categoria, disponible=True
    ).exclude(pk=pk)[:4]

    en_carrito = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            item = carrito.items.filter(producto=producto).first()
            if item:
                en_carrito = item.cantidad
        except Carrito.DoesNotExist:
            pass

    return render(request, 'store/detalle_producto.html', {
        'producto': producto,
        'imagenes': producto.get_imagenes(),
        'colores': producto.get_colores(),
        'tallas': producto.get_tallas(),
        'productos_relacionados': productos_relacionados,
        'en_carrito': en_carrito,
    })


@login_required
def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id, disponible=True)
    carrito, _ = Carrito.objects.get_or_create(usuario=request.user)
    item, created = CarritoItem.objects.get_or_create(carrito=carrito, producto=producto)
    if not created:
        if item.cantidad < producto.stock:
            item.cantidad += 1
            item.save()
    else:
        item.cantidad = 1
        item.save()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'total_items': carrito.total_items()})
    messages.success(request, f'"{producto.nombre}" agregado al carrito.')
    return redirect('catalogo')


@login_required
def quitar_carrito(request, producto_id):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        item = CarritoItem.objects.get(carrito=carrito, producto_id=producto_id)
        if item.cantidad > 1:
            item.cantidad -= 1
            item.save()
        else:
            item.delete()
    except (Carrito.DoesNotExist, CarritoItem.DoesNotExist):
        pass
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            return JsonResponse({'success': True, 'total_items': carrito.total_items()})
        except Carrito.DoesNotExist:
            return JsonResponse({'success': True, 'total_items': 0})
    return redirect('catalogo')


@login_required
def eliminar_item_carrito(request, producto_id):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        CarritoItem.objects.filter(carrito=carrito, producto_id=producto_id).delete()
    except Carrito.DoesNotExist:
        pass
    return redirect('envio')


@login_required
def envio(request):
    try:
        carrito = Carrito.objects.get(usuario=request.user)
        items = carrito.items.select_related('producto').all()
    except Carrito.DoesNotExist:
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('catalogo')

    if not items.exists():
        messages.error(request, 'Tu carrito está vacío.')
        return redirect('catalogo')

    subtotal = carrito.total()
    costo_envio = 100
    total = subtotal + costo_envio

    if request.method == 'POST':
        form = EnvioForm(request.POST)
        if form.is_valid():
            orden = Orden.objects.create(
                usuario=request.user,
                nombre_envio=form.cleaned_data['nombre_envio'],
                direccion=form.cleaned_data['direccion'],
                ciudad=form.cleaned_data['ciudad'],
                estado_envio=form.cleaned_data['estado_envio'],
                codigo_postal=form.cleaned_data['codigo_postal'],
                metodo_pago=form.cleaned_data['metodo_pago'],
                subtotal=subtotal,
                costo_envio=costo_envio,
                total=total,
            )
            for item in items:
                OrdenItem.objects.create(
                    orden=orden,
                    producto=item.producto,
                    cantidad=item.cantidad,
                    precio_unitario=item.producto.precio,
                )
                item.producto.stock -= item.cantidad
                item.producto.save()
            Factura.objects.create(orden=orden, total=total)
            carrito.items.all().delete()
            messages.success(request, f'¡Orden #{orden.id} confirmada!')
            return redirect('mis_ordenes')
    else:
        nombre_inicial = request.user.nombre_completo or request.user.username
        form = EnvioForm(initial={'nombre_envio': nombre_inicial})

    return render(request, 'store/envio.html', {
        'form': form, 'items': items,
        'subtotal': subtotal, 'costo_envio': costo_envio, 'total': total,
    })


@login_required
def mis_ordenes(request):
    ordenes = Orden.objects.filter(usuario=request.user).order_by('-fecha')
    return render(request, 'store/ordenes.html', {'ordenes': ordenes})


@login_required
def mis_facturas(request):
    facturas = Factura.objects.filter(orden__usuario=request.user).order_by('-fecha_emision')
    return render(request, 'store/facturas.html', {'facturas': facturas})


def ubicaciones(request):
    return render(request, 'store/ubicaciones.html')


# ── ADMIN ─────────────────────────────────────────────────────

@admin_required
def admin_dashboard(request):
    total_productos = Producto.objects.count()
    total_ordenes = Orden.objects.count()
    total_ventas = Orden.objects.filter(
        estado__in=['aprobado', 'enviado', 'entregado']
    ).aggregate(total=Sum('total'))['total'] or 0
    total_clientes = Usuario.objects.filter(rol='cliente').count()
    ultimas_ordenes = Orden.objects.select_related('usuario').order_by('-fecha')[:10]
    return render(request, 'admin_panel/dashboard.html', {
        'total_productos': total_productos,
        'total_ordenes': total_ordenes,
        'total_ventas': total_ventas,
        'total_clientes': total_clientes,
        'ultimas_ordenes': ultimas_ordenes,
    })


@admin_required
def admin_productos(request):
    query = request.GET.get('q', '')
    productos = Producto.objects.all().order_by('-fecha_creacion')
    if query:
        productos = productos.filter(
            Q(nombre__icontains=query) | Q(categoria__nombre__icontains=query)
        )
    paginator = Paginator(productos, 10)
    page = request.GET.get('page', 1)
    productos_page = paginator.get_page(page)
    return render(request, 'admin_panel/productos.html', {
        'productos': productos_page, 'query': query,
    })


@admin_required
def registrar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save(commit=False)
            producto.disponible = 'disponible' in request.POST
            producto.save()
            messages.success(request, f'Producto "{producto.nombre}" registrado.')
            return redirect('/admin/productos/')
        else:
            messages.error(request, 'Corrige los errores.')
    else:
        form = ProductoForm(initial={'disponible': True})
    return render(request, 'admin_panel/registrar_producto.html', {
        'form': form, 'titulo': 'Registrar Producto',
    })


@admin_required
def actualizar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            prod = form.save(commit=False)
            prod.disponible = 'disponible' in request.POST
            prod.save()
            messages.success(request, f'Producto actualizado.')
            return redirect('/admin/productos/')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'admin_panel/registrar_producto.html', {
        'form': form, 'titulo': 'Actualizar Producto', 'producto': producto,
    })


@admin_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre}" eliminado.')
        return redirect('/admin/productos/')
    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': producto, 'tipo': 'producto',
    })


@admin_required
def admin_pedidos(request):
    ordenes = Orden.objects.select_related('usuario').order_by('-fecha')
    return render(request, 'admin_panel/pedidos.html', {'ordenes': ordenes})


@admin_required
def aprobar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    orden.estado = 'aprobado'
    orden.save()
    messages.success(request, f'Orden #{orden.id} aprobada.')
    return redirect('/admin/pedidos/')


@admin_required
def eliminar_orden(request, pk):
    orden = get_object_or_404(Orden, pk=pk)
    if request.method == 'POST':
        orden.delete()
        messages.success(request, f'Orden #{pk} eliminada.')
        return redirect('/admin/pedidos/')
    return render(request, 'admin_panel/confirmar_eliminar.html', {
        'objeto': orden, 'tipo': 'orden',
    })

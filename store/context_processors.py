from .models import Carrito
from accounts.models import Administrador


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            count = carrito.total_items()
        except Carrito.DoesNotExist:
            count = 0
    return {'cart_count': count}


def admin_context(request):
    """Agrega info del admin de sesión a todos los templates."""
    es_admin = request.session.get('es_admin', False)
    admin_username = request.session.get('admin_username', '')
    admin_nombre = request.session.get('admin_nombre', '')
    return {
        'es_admin_sesion': es_admin,
        'admin_username': admin_username,
        'admin_nombre': admin_nombre,
    }

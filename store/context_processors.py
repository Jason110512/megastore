from .models import Carrito


def cart_count(request):
    count = 0
    if request.user.is_authenticated:
        try:
            carrito = Carrito.objects.get(usuario=request.user)
            count = carrito.total_items()
        except Carrito.DoesNotExist:
            count = 0
    return {'cart_count': count}

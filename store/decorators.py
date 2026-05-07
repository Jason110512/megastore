from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def admin_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        # Verificar sesión de admin separada
        if request.session.get('es_admin'):
            return view_func(request, *args, **kwargs)
        # Verificar usuario Django con rol admin
        if request.user.is_authenticated and request.user.is_admin_store():
            return view_func(request, *args, **kwargs)
        messages.error(request, 'No tienes permisos para acceder.')
        return redirect('/catalogo/')
    return wrapper


def cliente_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login/')
        return view_func(request, *args, **kwargs)
    return wrapper

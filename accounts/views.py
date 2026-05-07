from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import RegistroForm, UsuarioAdminForm
from .models import Usuario, Administrador
from store.decorators import admin_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/catalogo/')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        # ── Primero buscar en tabla Administrador ──────────────
        try:
            admin = Administrador.objects.get(username=username, activo=True)
            if admin.check_password(password):
                # Guardar en sesión como admin
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                request.session['admin_nombre'] = admin.nombre
                request.session['es_admin'] = True
                request.session.save()
                return redirect('/admin/dashboard/')
        except Administrador.DoesNotExist:
            pass

        # ── Luego buscar en tabla Usuario (clientes) ───────────
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return redirect('/catalogo/')
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'accounts/login.html', {'error': error})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('/catalogo/')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('/catalogo/')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})


def logout_view(request):
    # Cerrar sesión de admin
    if 'es_admin' in request.session:
        request.session.flush()
    # Cerrar sesión de cliente
    if request.user.is_authenticated:
        logout(request)
    return redirect('/accounts/login/')

@admin_required
def gestion_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'admin_panel/usuarios.html', {'usuarios': usuarios})


@admin_required
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.activo = not usuario.activo
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.activo else 'desactivado'
        messages.success(request, f'Usuario {usuario.username} {estado}.')
    return redirect('/accounts/usuarios/')


@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado.')
            return redirect('/accounts/usuarios/')
    else:
        form = UsuarioAdminForm(instance=usuario)
    return render(request, 'admin_panel/editar_usuario.html', {'form': form, 'usuario': usuario})


@admin_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
    return redirect('/accounts/usuarios/')
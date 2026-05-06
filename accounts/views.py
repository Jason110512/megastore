from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import LoginForm, RegistroForm, UsuarioAdminForm
from .models import Usuario
from store.decorators import admin_required


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_admin_store():
            return redirect('admin_dashboard')
        return redirect('catalogo')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        from django.contrib.auth import authenticate, login
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_admin_store():
                return redirect('admin_dashboard')
            return redirect('catalogo')
        else:
            error = 'Usuario o contraseña incorrectos.'

    return render(request, 'accounts/login.html', {'error': error})


def registro_view(request):
    if request.user.is_authenticated:
        return redirect('catalogo')

    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '¡Cuenta creada exitosamente!')
            return redirect('catalogo')
        else:
            messages.error(request, 'Por favor corrige los errores.')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registro.html', {'form': form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada.')
    return redirect('login')


@login_required
@admin_required
def gestion_usuarios(request):
    usuarios = Usuario.objects.all().order_by('-fecha_registro')
    return render(request, 'admin_panel/usuarios.html', {'usuarios': usuarios})


@login_required
@admin_required
def toggle_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.activo = not usuario.activo
        usuario.is_active = not usuario.is_active
        usuario.save()
        estado = 'activado' if usuario.activo else 'desactivado'
        messages.success(request, f'Usuario {usuario.username} {estado}.')
    return redirect('gestion_usuarios')


@login_required
@admin_required
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if request.method == 'POST':
        form = UsuarioAdminForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado.')
            return redirect('gestion_usuarios')
    else:
        form = UsuarioAdminForm(instance=usuario)
    return render(request, 'admin_panel/editar_usuario.html', {'form': form, 'usuario': usuario})


@login_required
@admin_required
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    if usuario != request.user:
        usuario.delete()
        messages.success(request, 'Usuario eliminado.')
    return redirect('gestion_usuarios')

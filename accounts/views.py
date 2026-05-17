from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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

        try:
            admin = Administrador.objects.get(username=username, activo=True)
            if admin.check_password(password):
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                request.session['admin_nombre'] = admin.nombre
                request.session['es_admin'] = True
                request.session.save()
                return redirect('/admin/dashboard/')
        except Administrador.DoesNotExist:
            pass

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
    if 'es_admin' in request.session:
        request.session.flush()
    if request.user.is_authenticated:
        logout(request)
    return redirect('/accounts/login/')


@login_required
def perfil(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre_completo', '').strip()
        correo = request.POST.get('correo', '').strip()
        if nombre:
            request.user.nombre_completo = nombre
        if correo:
            request.user.correo = correo
            request.user.email = correo
        request.user.save()
        messages.success(request, 'Perfil actualizado correctamente.')
        return redirect('/accounts/perfil/')
    return render(request, 'accounts/perfil.html', {'usuario': request.user})


@login_required
def cambiar_password(request):
    error = None
    if request.method == 'POST':
        password_actual = request.POST.get('password_actual')
        password_nueva = request.POST.get('password_nueva')
        password_confirm = request.POST.get('password_confirm')

        if not request.user.check_password(password_actual):
            error = 'La contraseña actual es incorrecta.'
        elif password_nueva != password_confirm:
            error = 'Las contraseñas nuevas no coinciden.'
        elif len(password_nueva) < 6:
            error = 'La contraseña debe tener al menos 6 caracteres.'
        else:
            request.user.set_password(password_nueva)
            request.user.save()
            login(request, request.user)
            messages.success(request, '¡Contraseña cambiada exitosamente!')
            return redirect('/accounts/perfil/')

    return render(request, 'accounts/cambiar_password.html', {'error': error})


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

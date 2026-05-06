from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ('username', 'nombre_completo', 'correo', 'rol', 'activo', 'fecha_registro')
    list_filter = ('rol', 'activo', 'is_staff')
    search_fields = ('username', 'nombre_completo', 'correo')
    ordering = ('-fecha_registro',)
    fieldsets = UserAdmin.fieldsets + (
        ('Datos Mega Store', {'fields': ('nombre_completo', 'correo', 'rol', 'activo')}),
    )

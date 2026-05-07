#!/usr/bin/env python
"""
Crea un administrador en la tabla Administrador.
Uso: python3 crear_admin.py
"""
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import Administrador

# Eliminar admin anterior si existe
Administrador.objects.filter(username='admin').delete()

# Crear nuevo admin
admin = Administrador(
    nombre='Administrador',
    username='admin',
    correo='admin@megastore.com',
    activo=True,
)
admin.set_password('Admin2024')
admin.save()

print("✅ Administrador creado:")
print(f"   Usuario: admin")
print(f"   Contraseña: Admin2024")
print(f"   URL: /admin/dashboard/")

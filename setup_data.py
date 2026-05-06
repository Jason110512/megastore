#!/usr/bin/env python
"""
Script de configuración inicial para Mega Store.
Ejecutar después de las migraciones: python setup_data.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from accounts.models import Usuario
from store.models import Categoria, Producto

print("=== Configurando datos iniciales de Mega Store ===\n")

# Categorías
categorias_data = [
    ("Electronica", "Productos electrónicos y gadgets"),
    ("Ropa", "Ropa y moda"),
    ("Deportes", "Artículos deportivos"),
    ("Hogar", "Artículos para el hogar"),
]
for nombre, desc in categorias_data:
    cat, created = Categoria.objects.get_or_create(nombre=nombre, defaults={"descripcion": desc})
    if created:
        print(f"  ✓ Categoría creada: {nombre}")

# Productos de ejemplo
electronica = Categoria.objects.get(nombre="Electronica")
productos_data = [
    {
        "nombre": "Smartwatch",
        "descripcion": "Resistente al agua. Colores (Rosa, Azul, Verde, Negro)",
        "precio": 600,
        "stock": 8,
        "estrellas": 4,
        "categoria": electronica,
    },
    {
        "nombre": "Audífonos Sony WH-CH520 Wireless",
        "descripcion": "Hasta 50 horas de reproducción continua. Excelente claridad de voz para llamadas.",
        "precio": 800,
        "stock": 40,
        "estrellas": 5,
        "categoria": electronica,
    },
    {
        "nombre": "iPhone 16 pro max",
        "descripcion": "Resistente al agua. El mejor smartphone del mercado.",
        "precio": 25000,
        "stock": 54,
        "estrellas": 4,
        "categoria": electronica,
    },
]
for p in productos_data:
    obj, created = Producto.objects.get_or_create(nombre=p["nombre"], defaults=p)
    if created:
        print(f"  ✓ Producto creado: {p['nombre']}")

# Superusuario admin
if not Usuario.objects.filter(username="admin").exists():
    admin = Usuario.objects.create_superuser(
        username="admin",
        password="admin123",
        email="admin@megastore.com",
        nombre_completo="Administrador",
        rol="admin",
    )
    print("\n  ✓ Administrador creado:")
    print("    Usuario: admin")
    print("    Contraseña: admin123")
else:
    print("\n  ℹ️  El usuario 'admin' ya existe.")

# Cliente de prueba
if not Usuario.objects.filter(username="cliente1").exists():
    cliente = Usuario.objects.create_user(
        username="cliente1",
        password="cliente123",
        email="cliente1@megastore.com",
        nombre_completo="Cliente Demo",
        rol="cliente",
    )
    print("\n  ✓ Cliente de prueba creado:")
    print("    Usuario: cliente1")
    print("    Contraseña: cliente123")
else:
    print("  ℹ️  El usuario 'cliente1' ya existe.")

print("\n=== ¡Configuración completa! ===")
print("\nPuedes iniciar el servidor con:")
print("  python manage.py runserver")

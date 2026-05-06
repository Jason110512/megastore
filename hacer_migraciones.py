#!/usr/bin/env python
"""
Ejecutar este script para aplicar los nuevos campos del modelo Producto:
- imagen2, imagen3, imagen4
- precio_original
- colores, tallas
- envio_gratis, meses_sin_intereses
- num_resenas

Uso: python3 hacer_migraciones.py
"""
import os
import subprocess
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

print("=== Aplicando migraciones de nuevos campos ===\n")

cmds = [
    [sys.executable, 'manage.py', 'makemigrations', 'store', '--name', 'producto_campos_nuevos'],
    [sys.executable, 'manage.py', 'migrate'],
]

for cmd in cmds:
    print(f"▶ {' '.join(cmd)}")
    result = subprocess.run(cmd)
    if result.returncode != 0:
        print(f"\n❌ Error ejecutando: {' '.join(cmd)}")
        sys.exit(1)
    print()

print("✅ ¡Migraciones aplicadas correctamente!")
print("\nAhora reinicia el servidor:")
print("  python3 manage.py runserver")

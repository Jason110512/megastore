#!/bin/bash
# =============================================
#  MEGA STORE — Script de instalación rápida
#  Ejecutar: bash install.sh
# =============================================

echo ""
echo "🛍️  ============================================"
echo "    MEGA STORE — Instalación"
echo "    ============================================"
echo ""

# 1. Entorno virtual
echo "📦 Creando entorno virtual..."
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 2. Dependencias
echo "📥 Instalando dependencias..."
pip install -r requirements.txt

# 3. PostgreSQL — solicitar datos de conexión
echo ""
echo "🗄️  Configuración de PostgreSQL"
echo "   (Presiona Enter para usar valores predeterminados)"
read -p "   DB_NAME [megastore_db]: " DB_NAME
read -p "   DB_USER [postgres]: " DB_USER
read -p "   DB_PASSWORD [postgres]: " DB_PASSWORD
read -p "   DB_HOST [localhost]: " DB_HOST
read -p "   DB_PORT [5432]: " DB_PORT

export DB_NAME=${DB_NAME:-megastore_db}
export DB_USER=${DB_USER:-postgres}
export DB_PASSWORD=${DB_PASSWORD:-postgres}
export DB_HOST=${DB_HOST:-localhost}
export DB_PORT=${DB_PORT:-5432}

# 4. Migraciones
echo ""
echo "🔄 Ejecutando migraciones..."
python manage.py makemigrations accounts
python manage.py makemigrations store
python manage.py migrate

# 5. Datos iniciales
echo ""
echo "🌱 Cargando datos iniciales..."
python setup_data.py

# 6. Colectar estáticos
echo ""
echo "📁 Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo ""
echo "✅ ============================================"
echo "   ¡Instalación completada!"
echo ""
echo "   Accesos:"
echo "   👤 Admin:    admin / admin123"
echo "   👤 Cliente:  cliente1 / cliente123"
echo ""
echo "   Iniciar servidor:"
echo "   python manage.py runserver"
echo ""
echo "   URL: http://localhost:8000"
echo "   ============================================"
echo ""

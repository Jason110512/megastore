@echo off
REM =============================================
REM  MEGA STORE — Script de instalacion (Windows)
REM  Ejecutar: install.bat
REM =============================================

echo.
echo  MEGA STORE - Instalacion
echo  ============================================
echo.

REM Entorno virtual
echo Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate

REM Dependencias
echo Instalando dependencias...
pip install -r requirements.txt

REM Variables de entorno (edita estos valores si es necesario)
set DB_NAME=megastore_db
set DB_USER=postgres
set DB_PASSWORD=postgres
set DB_HOST=localhost
set DB_PORT=5432

REM Migraciones
echo Ejecutando migraciones...
python manage.py makemigrations accounts
python manage.py makemigrations store
python manage.py migrate

REM Datos iniciales
echo Cargando datos iniciales...
python setup_data.py

REM Estaticos
echo Recolectando archivos estaticos...
python manage.py collectstatic --noinput

echo.
echo  Instalacion completada!
echo.
echo  Accesos:
echo  Admin:   admin / admin123
echo  Cliente: cliente1 / cliente123
echo.
echo  Iniciando servidor...
python manage.py runserver

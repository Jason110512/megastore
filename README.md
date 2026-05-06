# 🛍️ MEGA STORE — Sistema E-Commerce Django + PostgreSQL

## Estructura del Proyecto

```
megastore/
├── core/               # Configuración Django
│   ├── settings.py     # Variables de entorno y DB
│   └── urls.py         # URL principal
├── accounts/           # App de usuarios
│   ├── models.py       # Modelo Usuario personalizado
│   ├── views.py        # Login, registro, gestión usuarios
│   ├── forms.py        # Formularios de autenticación
│   └── urls.py
├── store/              # App principal de la tienda
│   ├── models.py       # Producto, Orden, Carrito, Factura
│   ├── views.py        # Todas las vistas (cliente + admin)
│   ├── forms.py        # Formularios de envío y producto
│   ├── urls.py
│   ├── decorators.py   # @admin_required
│   └── context_processors.py  # cart_count global
├── templates/
│   ├── base.html       # Layout base (sidebar + topbar)
│   ├── accounts/
│   │   ├── login.html
│   │   └── registro.html
│   ├── store/
│   │   ├── catalogo.html
│   │   ├── envio.html
│   │   ├── ordenes.html
│   │   ├── facturas.html
│   │   └── ubicaciones.html
│   └── admin_panel/
│       ├── dashboard.html
│       ├── productos.html
│       ├── registrar_producto.html
│       ├── pedidos.html
│       ├── usuarios.html
│       └── confirmar_eliminar.html
├── setup_data.py       # Script para datos iniciales
├── requirements.txt
└── manage.py
```

---

## ⚙️ Instalación Paso a Paso

### 1. Prerrequisitos
- Python 3.10+
- PostgreSQL 14+
- pip

### 2. Crear y activar entorno virtual
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Crear base de datos en PostgreSQL
```sql
-- Abre psql y ejecuta:
CREATE DATABASE megastore_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE megastore_db TO postgres;
```

### 5. Configurar variables de entorno (opcional)
Puedes crear un archivo `.env` o exportar variables:
```bash
export DB_NAME=megastore_db
export DB_USER=postgres
export DB_PASSWORD=postgres
export DB_HOST=localhost
export DB_PORT=5432
```

O editar directamente `core/settings.py` con tus credenciales.

### 6. Ejecutar migraciones
```bash
python manage.py makemigrations accounts
python manage.py makemigrations store
python manage.py migrate
```

### 7. Cargar datos iniciales
```bash
python setup_data.py
```

Esto crea:
- 👤 Admin: `admin` / `admin123`
- 👤 Cliente: `cliente1` / `cliente123`
- 📦 3 productos de ejemplo
- 🗂️ 4 categorías

### 8. Iniciar servidor
```bash
python manage.py runserver
```

Accede en: **http://localhost:8000**

---

## 🔐 Roles y Accesos

| Rol | Usuario | Vistas |
|-----|---------|--------|
| Admin | admin | Dashboard, Gestión Productos, Pedidos, Usuarios |
| Cliente | cliente1 | Catálogo, Carrito, Envío, Mis Órdenes, Facturas |

---

## 📱 URLs Principales

### Cliente
| URL | Vista |
|-----|-------|
| `/accounts/login/` | Inicio de sesión |
| `/accounts/registro/` | Registro |
| `/catalogo/` | Catálogo de productos |
| `/envio/` | Checkout / información de envío |
| `/mis-ordenes/` | Historial de órdenes |
| `/mis-facturas/` | Facturas |
| `/ubicaciones/` | Sucursales |

### Admin
| URL | Vista |
|-----|-------|
| `/admin/dashboard/` | Panel principal |
| `/admin/productos/` | Lista de productos |
| `/admin/productos/registrar/` | Nuevo producto |
| `/admin/productos/<id>/actualizar/` | Editar producto |
| `/admin/productos/<id>/eliminar/` | Eliminar producto |
| `/admin/pedidos/` | Gestión de pedidos |
| `/accounts/usuarios/` | Gestión de usuarios |

---

## 🗄️ Modelos de Base de Datos

- **Usuario** — Extiende AbstractUser con rol (cliente/admin)
- **Categoria** — Categorías de productos
- **Producto** — Catálogo con imagen, precio, stock, estrellas
- **Carrito / CarritoItem** — Carrito de compras por usuario
- **Orden / OrdenItem** — Pedidos confirmados con datos de envío
- **Factura** — Comprobante automático por cada orden

---

## 🚀 Tecnologías

- **Backend:** Django 4.2 + Python
- **Base de datos:** PostgreSQL
- **Frontend:** Bootstrap 5 + Font Awesome 6 + Google Fonts
- **Archivos:** Pillow (imágenes), WhiteNoise (archivos estáticos)

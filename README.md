# StockZ

StockZ es el proyecto base para un sistema de gestión de catálogo en Django con autenticación nativa, usando templates server-rendered y Bootstrap 5. Este repositorio queda como esqueleto inicial y no incluye aún los ABM funcionales ni el sistema completo.

## Objetivo de la base

- Python 3
- Django
- Django Templates
- Bootstrap 5
- SQLite como base por defecto para desarrollo y demostración local
- PostgreSQL como alternativa futura para entornos más avanzados
- ORM de Django
- autenticación nativa con sesiones, grupos y permisos
- pytest + pytest-django

## Comparación con StockX

### Estructura real observada en StockX

Se verificó que en la carpeta fuente `C:\GitHub\Facultad\TIF\StockX\backend` existe una aplicación Django con:

- `config/settings.py`
- `config/urls.py`
- `authentication/models.py`
- `authentication/views.py`
- `inventario/models.py`
- `inventario/views.py`
- `inventario/permissions.py`
- `ventas/` y `dashboard/`
- `requirements.txt`

El proyecto de origen usa:

- Django + DRF + JWT
- `AUTH_USER_MODEL = 'authentication.Usuario'`
- roles hardcodeados en `Usuario.rol`
- API REST con ViewSets
- catálogo y negocio con elementos de ventas, alertas y compras no incluidos en StockZ

### Qué se adapta a StockZ

- Modelo de catálogo: `Categoria`, `Proveedor` y `Producto` son la base reutilizable.
- Validaciones de negocio compatibles: precios no negativos, stock no negativo, `activo`, `unique` y reglas de integridad.
- Organización por apps y settings centralizados.
- Uso de Django Templates en lugar de SPA/REST.

### Qué se reconstruye

- Autenticación nativa de Django, con `User`/`Group`/`Permission` y sesiones.
- Roles `Administrador` y `Empleado` como grupos de Django, no como campo `rol` en un custom user.
- Vistas y URLs server-side, no API REST + JWT.
- ABM de productos, categorías y proveedores aún pendientes.
- Todo lo excluido: ventas, movimientos, dashboard, alertas, historial de compras, `ProductoProveedor`, `precio_costo`, etc.

## Reutilización de StockX

### Referencias originales consultadas

- `C:\GitHub\Facultad\TIF\StockX\backend\config\settings.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\authentication\models.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\authentication\serializers.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\authentication\views.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\inventario\models.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\inventario\permissions.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\inventario\views.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\inventario\urls.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\config\urls.py`
- `C:\GitHub\Facultad\TIF\StockX\backend\requirements.txt`

## Estructura creada en StockZ

- `manage.py`
- `requirements.txt`
- `pytest.ini`
- `.env.example`
- `README.md`
- `stockz/settings.py`
- `stockz/urls.py`
- `stockz/asgi.py`
- `stockz/wsgi.py`
- `apps/__init__.py`
- `apps/catalogo/...`
- `apps/usuarios/...`
- `templates/base.html`
- `templates/home.html`
- `templates/registration/login.html`
- `docs/stockx_reuse.md`

## Adaptaciones necesarias

1. Reemplazar `AUTH_USER_MODEL` por el `User` nativo de Django.
2. Usar grupos `Administrador` y `Empleado` en vez de `rol` en `Usuario`.
3. Eliminar `JWT` y `SimpleJWT` del baseline de StockZ.
4. Reemplazar `DRF ViewSet` por vistas de Django Template.
5. Excluir `ProductoProveedor`, `precio_costo`, compras e historial.
6. Mantener solamente el catálogo y la autenticación requerida.

## Estado actual

Este esqueleto deja la base lista para continuar con la parte funcional en una segunda etapa, sin implementar aún ABM, login empresarial completo ni módulos excluidos.

Para demostración local y desarrollo inicial, el proyecto se ejecuta con SQLite de manera sencilla y sin requerir PostgreSQL. PostgreSQL queda como opción futura para despliegues o entornos de producción más complejos.

## Usuarios de demostración

Los grupos `Administrador` y `Empleado` se crean automáticamente al migrar la base de datos.

### Crear usuarios de prueba con Django Admin

1. Ejecutá la base local:

```bash
python manage.py migrate
python manage.py runserver
```

2. Creá un superusuario si aún no existe:

```bash
python manage.py createsuperuser
```

3. Entrá al panel administrativo en `http://127.0.0.1:8000/admin/`.
4. Creá dos usuarios, por ejemplo:
   - `admin_demo` → asignar grupo `Administrador`
   - `empleado_demo` → asignar grupo `Empleado`
5. Iniciá sesión con cada usuario en la pantalla de login del sistema.

Los permisos de cada grupo se asignan desde Django y se validan en el backend, no sólo en la interfaz.

## Verificaciones realizadas

Se ejecutó una verificación sintáctica sobre la estructura creada con:

```bash
python -m compileall "C:\GitHub\Facultad\StockZ"
```

La comprobación de sintaxis debe devolver salida exitosa y sin errores de compilación.

> No se tocaron archivos del proyecto origen `StockX`.

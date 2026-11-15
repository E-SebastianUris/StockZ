# StockZ

Repositorio: https://github.com/E-SebastianUris/StockZ

StockZ es una aplicación web desarrollada en Django para organizar y consultar el catálogo de un kiosco. El sistema centraliza la información de productos, categorías y proveedores, y controla el acceso a la información según el rol del usuario autenticado.

## Problema que resuelve

En un kiosco, la información de productos, categorías y proveedores suele distribuirse entre listados, hojas de cálculo y registros informales. Esto dificulta:

- consultar en forma rápida qué productos están disponibles,
- mantener una estructura clara por categoría,
- identificar proveedores y sus datos de contacto,
- controlar quién puede ver o modificar la información del catálogo.

StockZ propone una solución web para centralizar ese catálogo y establecer permisos por perfil de usuario.

## Solución propuesta

StockZ es una aplicación web de gestión del catálogo del kiosco. Permite:

- autenticar usuarios con el sistema nativo de Django,
- definir roles mediante grupos,
- controlar permisos del backend,
- consultar productos, categorías y proveedores,
- mantener una separación de acceso entre administradores y empleados.

## Objetivos del sistema

- centralizar la información del catálogo del kiosco,
- facilitar la consulta de productos, categorías y proveedores,
- diferenciar permisos por rol,
- mantener un sistema simple y operativo en entorno local,
- usar Django como base para autenticación, autorización y gestión del catálogo.

## Funcionalidades implementadas

En su estado actual, StockZ incluye lo siguiente:

- inicio y cierre de sesión,
- roles `Administrador` y `Empleado`,
- administración de permisos a través de grupos de Django,
- consulta de productos, categorías y proveedores,
- restricción de operaciones de escritura para usuarios con rol Empleado,
- carga de datos de demostración para iniciar la aplicación con información base.

## Roles y permisos

Los grupos `Administrador` y `Empleado` se crean automáticamente después de ejecutar las migraciones.

- `Administrador`: cuenta con permisos de consulta y de escritura configurados en Django para el catálogo.
- `Empleado`: puede consultar productos, categorías y proveedores, pero no ejecutar operaciones de alta, edición ni eliminación.

La validación real de permisos se realiza en el backend con Django y el decorador `permission_required`.

### Importante sobre permisos CRUD

Los permisos CRUD del grupo `Administrador` están configurados en Django, pero los flujos completos de alta, edición y eliminación aún no están implementados operativamente en la aplicación. La seguridad por permisos existe en el backend, pero la funcionalidad completa de creación y edición del catálogo no está finalizada como flujo de negocio completo.

### Superusuario y asignación de grupo

La creación de un superusuario no lo incorpora automáticamente al grupo `Administrador`.

Para asignar el rol correcto, se debe:

1. crear el superusuario con `python manage.py createsuperuser`,
2. ingresar a Django Admin,
3. abrir el usuario creado,
4. asignarle el grupo `Administrador` desde la sección de grupos.

## Tecnologías utilizadas

StockZ utiliza las siguientes tecnologías principales:

- Python
- Django
- Django ORM
- SQLite como base de datos actual para el entorno local
- Bootstrap 5 para la interfaz web
- pytest y pytest-django para pruebas automatizadas

### Base de datos

La base de datos utilizada actualmente es SQLite, que es la configuración por defecto para desarrollo local y pruebas. PostgreSQL puede considerarse como alternativa prevista para entornos más avanzados, pero no es necesaria para ejecutar el proyecto en este estado actual.

## Modelo de datos

El proyecto define tres modelos dentro del catálogo.

### Categoría

Representa una agrupación de productos.

- `nombre`: nombre único de la categoría.
- `descripcion`: texto descriptivo opcional.
- `activo`: indica si la categoría está activa.
- `creado_el` y `actualizado_el`: timestamps de auditoría.

### Producto

Representa un artículo del catálogo del kiosco.

- `nombre`
- `codigo_barra`: valor único opcional.
- `descripcion`
- `categoria`: relación `ForeignKey` hacia `Categoria`.
- `precio_venta`
- `stock_actual`
- `stock_minimo`
- `activo`
- `creado_el` y `actualizado_el`

Relación real implementada:

- cada `Producto` pertenece a una sola `Categoria`;
- una `Categoria` puede tener varios `Producto` asociados.

Se aplican validaciones para asegurar que `precio_venta`, `stock_actual` y `stock_minimo` no sean negativos.

### Proveedor

Representa a la entidad que suministra productos o insumos.

- `nombre`
- `contacto`
- `telefono`
- `email`
- `direccion`
- `cuit`: identificador único opcional.
- `activo`
- `creado_el` y `actualizado_el`

En esta implementación, no existe una relación de compra ni de asociación histórica entre `Proveedor` y `Producto`; cada entidad se conserva de manera independiente dentro del catálogo.

## Instalación y configuración

### Requisitos

- Python instalado en el sistema.
- acceso a la línea de comandos.

### 1. Clonar el repositorio

```bash
git clone https://github.com/E-SebastianUris/StockZ
cd StockZ
```

### 2. Crear un entorno virtual

En Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

En macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

El proyecto usa SQLite por defecto para desarrollo local. No es necesario configurar una base de datos externa para ejecutar el sistema en este estado actual.

PostgreSQL puede usarse como alternativa prevista en entornos más avanzados, pero no es requisito para correr el proyecto.

### 5. Ejecutar migraciones

```bash
python manage.py migrate
```

Esta operación crea las tablas del proyecto y también genera automáticamente los grupos `Administrador` y `Empleado`.

### 6. Crear un superusuario

```bash
python manage.py createsuperuser
```

Luego, desde Django Admin, se debe asignar el grupo `Administrador` al usuario correspondiente.

### 7. Cargar datos de demostración

```bash
python manage.py cargar_datos_demo
```

Este comando crea registros iniciales de categorías, proveedores y productos para probar la aplicación.

### 8. Levantar el servidor

```bash
python manage.py runserver
```

Luego se puede acceder en:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/admin/

## Ejecución de pruebas

El proyecto incluye pruebas automatizadas con `pytest` y `pytest-django`.

Para ejecutar la suite actual:

```bash
python -m pytest -q
```

Las pruebas cubren la autenticación, el login y logout, el acceso a páginas protegidas, los permisos por rol y la consulta del catálogo.

## Estado actual y funcionalidades pendientes

StockZ se encuentra en una etapa inicial orientada a la gestión del catálogo y al control de acceso del kiosco.

### Implementado

- autenticación con usuarios y sesiones de Django,
- login y logout,
- pantalla principal con información del usuario y su rol,
- grupos `Administrador` y `Empleado`,
- permisos por grupo para consultar y restringir operaciones,
- listado de productos, categorías y proveedores,
- carga de datos de demostración,
- pruebas automatizadas básicas.

### Pendiente

- los flujos completos de alta, edición y eliminación del catálogo no están finalizados operativamente,
- la seguridad por permisos sí está configurada en Django, pero la experiencia completa de administración no está implementada como un proceso completo del negocio,
- el proyecto no incluye módulos adicionales como ventas, compras, movimientos, dashboard o alertas.

En este punto, StockZ está orientado a la gestión del catálogo del kiosco y al control de acceso por rol, con foco en la consulta y la autorización.

## Resumen

StockZ es una aplicación web independiente para organizar y consultar el catálogo de un kiosco. Su propósito principal es centralizar la información del negocio, proteger el acceso según el perfil del usuario y facilitar la operación diaria del catálogo con una base sólida en Django y permisos nativos.

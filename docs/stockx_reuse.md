# Documento de reutilización StockX → StockZ

## Resumen ejecutivo

StockX contiene una base sólida de catálogo y una estructura Django clara, pero su diseño se orienta a API REST con JWT y a un negocio más amplio (ventas, compras, alertas y dashboard). Para StockZ, se reutiliza solo lo compatible con el alcance pedido y se reemplaza la capa de autenticación y renderizado por el stack nativo de Django.

## Compatibilidad directa

- Estructura de apps por dominio
- Configuración base de Django
- Patrones de validación de catálogo
- Uso de `Categoria`, `Proveedor`, `Producto` como base conceptual
- nombres y restricciones de integridad de negocio

## Adaptaciones obligatorias

- `authentication.Usuario` de StockX no es compatible porque StockZ exige autenticación Django nativa.
- `rol` como campo se reemplaza por grupos y permisos.
- `rest_framework_simplejwt` se elimina del stack de StockZ.
- `inventario.permissions.HasInventarioRolePermission` se reescribe con permisos de Django.
- `viewsets` y serializadores DRF se descartan para vistas con templates.

## Elementos descartados del proyecto origen

- `ventas/`
- `dashboard/`
- `ProductoProveedor`
- `precio_costo`
- alertas de stock y vencimiento
- movimientos de stock
- historial y compras
- multi-sucursal

## Esqueleto final

La base creada en StockZ busca dejar listo:

- `manage.py`
- settings del proyecto
- URLs principales
- templates base y login nativo
- apps `catalogo` y `usuarios`
- `pytest.ini` con pytest-django

## Regla de trabajo aplicada

- StockX queda en solo lectura.
- Todas las modificaciones se hacen en StockZ.
- No se inicializa Git ni se configuran remotos.
- No se implementan todavía ABM ni funcionalidad de negocio.

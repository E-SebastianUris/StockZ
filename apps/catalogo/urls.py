from django.urls import path

from . import views

app_name = 'catalogo'

urlpatterns = [
    path('productos/', views.producto_list, name='productos'),
    path('productos/crear/', views.producto_create, name='producto_crear'),
    path('productos/<int:pk>/editar/', views.producto_edit, name='producto_editar'),
    path('productos/<int:pk>/eliminar/', views.producto_delete, name='producto_eliminar'),
    path('categorias/', views.categoria_list, name='categorias'),
    path('categorias/crear/', views.categoria_create, name='categoria_crear'),
    path('categorias/<int:pk>/editar/', views.categoria_edit, name='categoria_editar'),
    path('categorias/<int:pk>/eliminar/', views.categoria_delete, name='categoria_eliminar'),
    path('proveedores/', views.proveedor_list, name='proveedores'),
    path('proveedores/crear/', views.proveedor_create, name='proveedor_crear'),
    path('proveedores/<int:pk>/editar/', views.proveedor_edit, name='proveedor_editar'),
    path('proveedores/<int:pk>/eliminar/', views.proveedor_delete, name='proveedor_eliminar'),
]

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Categoria, Producto, Proveedor


def get_user_role(user):
    if user.groups.filter(name='Administrador').exists():
        return 'Administrador'
    if user.groups.filter(name='Empleado').exists():
        return 'Empleado'
    return 'Sin rol'


@login_required
@permission_required('catalogo.view_producto', raise_exception=True)
def producto_list(request):
    productos = Producto.objects.select_related('categoria').all()
    return render(request, 'catalogo/productos.html', {
        'productos': productos,
        'title': 'Productos',
        'user_role': get_user_role(request.user),
        'is_admin': request.user.groups.filter(name='Administrador').exists(),
    })


@login_required
@permission_required('catalogo.add_producto', raise_exception=True)
def producto_create(request):
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear producto',
        'action': 'Crear',
        'object_type': 'producto',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_producto', raise_exception=True)
def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar producto',
        'action': 'Editar',
        'object_type': 'producto',
        'producto': producto,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.delete_producto', raise_exception=True)
def producto_delete(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('catalogo:productos')
    return render(request, 'catalogo/producto_delete.html', {
        'producto': producto,
        'title': 'Eliminar producto',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.view_categoria', raise_exception=True)
def categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'catalogo/categorias.html', {
        'categorias': categorias,
        'title': 'Categorías',
        'user_role': get_user_role(request.user),
        'is_admin': request.user.groups.filter(name='Administrador').exists(),
    })


@login_required
@permission_required('catalogo.add_categoria', raise_exception=True)
def categoria_create(request):
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear categoría',
        'action': 'Crear',
        'object_type': 'categoría',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_categoria', raise_exception=True)
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar categoría',
        'action': 'Editar',
        'object_type': 'categoría',
        'categoria': categoria,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.delete_categoria', raise_exception=True)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('catalogo:categorias')
    return render(request, 'catalogo/producto_delete.html', {
        'producto': None,
        'categoria': categoria,
        'title': 'Eliminar categoría',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.view_proveedor', raise_exception=True)
def proveedor_list(request):
    proveedores = Proveedor.objects.all()
    return render(request, 'catalogo/proveedores.html', {
        'proveedores': proveedores,
        'title': 'Proveedores',
        'user_role': get_user_role(request.user),
        'is_admin': request.user.groups.filter(name='Administrador').exists(),
    })


@login_required
@permission_required('catalogo.add_proveedor', raise_exception=True)
def proveedor_create(request):
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear proveedor',
        'action': 'Crear',
        'object_type': 'proveedor',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_proveedor', raise_exception=True)
def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar proveedor',
        'action': 'Editar',
        'object_type': 'proveedor',
        'proveedor': proveedor,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.delete_proveedor', raise_exception=True)
def proveedor_delete(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        proveedor.delete()
        return redirect('catalogo:proveedores')
    return render(request, 'catalogo/producto_delete.html', {
        'producto': None,
        'proveedor': proveedor,
        'title': 'Eliminar proveedor',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })

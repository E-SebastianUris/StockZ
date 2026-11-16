from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoriaForm, ProductoForm, ProveedorForm
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
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('catalogo:productos')
    else:
        form = ProductoForm()

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear producto',
        'action': 'Crear',
        'object_type': 'producto',
        'form': form,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_producto', raise_exception=True)
def producto_edit(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado correctamente.')
            return redirect('catalogo:productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar producto',
        'action': 'Guardar cambios',
        'object_type': 'producto',
        'form': form,
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
        messages.success(request, 'Producto eliminado correctamente.')
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
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada correctamente.')
            return redirect('catalogo:categorias')
    else:
        form = CategoriaForm()

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear categoría',
        'action': 'Crear',
        'object_type': 'categoría',
        'form': form,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_categoria', raise_exception=True)
def categoria_edit(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada correctamente.')
            return redirect('catalogo:categorias')
    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar categoría',
        'action': 'Guardar cambios',
        'object_type': 'categoría',
        'form': form,
        'categoria': categoria,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.delete_categoria', raise_exception=True)
def categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        if categoria.productos.exists():
            messages.error(request, 'No se puede eliminar la categoría porque tiene productos asociados.')
            return redirect('catalogo:categorias')
        try:
            categoria.delete()
            messages.success(request, 'Categoría eliminada correctamente.')
        except ProtectedError:
            messages.error(request, 'No se puede eliminar la categoría porque está asociada a productos.')
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
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor creado correctamente.')
            return redirect('catalogo:proveedores')
    else:
        form = ProveedorForm()

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Crear proveedor',
        'action': 'Crear',
        'object_type': 'proveedor',
        'form': form,
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })


@login_required
@permission_required('catalogo.change_proveedor', raise_exception=True)
def proveedor_edit(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado correctamente.')
            return redirect('catalogo:proveedores')
    else:
        form = ProveedorForm(instance=proveedor)

    return render(request, 'catalogo/producto_form.html', {
        'title': 'Editar proveedor',
        'action': 'Guardar cambios',
        'object_type': 'proveedor',
        'form': form,
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
        messages.success(request, 'Proveedor eliminado correctamente.')
        return redirect('catalogo:proveedores')
    return render(request, 'catalogo/producto_delete.html', {
        'producto': None,
        'proveedor': proveedor,
        'title': 'Eliminar proveedor',
        'user_role': get_user_role(request.user),
        'is_admin': True,
    })

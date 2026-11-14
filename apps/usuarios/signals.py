from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


@receiver(post_migrate)
def create_default_roles(sender, **kwargs):
    """Crea los grupos base de StockZ con permisos del catálogo."""
    # Se ejecuta tras cada migración, incluyendo las pruebas con pytest-django.

    admin_group, _ = Group.objects.get_or_create(name='Administrador')
    employee_group, _ = Group.objects.get_or_create(name='Empleado')

    admin_permissions = Permission.objects.filter(
        content_type__app_label='catalogo',
        codename__in=[
            'add_categoria', 'change_categoria', 'delete_categoria', 'view_categoria',
            'add_proveedor', 'change_proveedor', 'delete_proveedor', 'view_proveedor',
            'add_producto', 'change_producto', 'delete_producto', 'view_producto',
        ],
    )
    employee_permissions = Permission.objects.filter(
        content_type__app_label='catalogo',
        codename__in=['view_categoria', 'view_proveedor', 'view_producto'],
    )

    admin_group.permissions.set(admin_permissions)
    employee_group.permissions.set(employee_permissions)

from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    """Vista principal del sistema con información del usuario autenticado y su rol."""
    is_admin = request.user.groups.filter(name='Administrador').exists()
    is_employee = request.user.groups.filter(name='Empleado').exists()
    role = 'Administrador' if is_admin else 'Empleado' if is_employee else 'Sin rol'

    return render(request, 'home.html', {
        'title': 'StockZ',
        'user_role': role,
        'is_admin': is_admin,
        'is_employee': is_employee,
    })

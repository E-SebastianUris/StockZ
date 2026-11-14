from django.contrib import admin
from django.shortcuts import render
from django.urls import include, path


def permission_denied_view(request, exception=None):
    return render(request, '403.html', {
        'title': 'Acceso denegado',
        'message': 'No tienes permisos para acceder a esta sección.'
    }, status=403)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('apps.usuarios.urls')),
    path('catalogo/', include('apps.catalogo.urls')),
]

handler403 = 'stockz.urls.permission_denied_view'

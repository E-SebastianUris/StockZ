from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse

from apps.catalogo.models import Categoria, Producto, Proveedor

User = get_user_model()


@pytest.fixture
def admin_user(db):
    user = User.objects.create_user(username='admin_demo', password='Pass123!')
    group = Group.objects.get(name='Administrador')
    user.groups.add(group)
    return user


@pytest.fixture
def employee_user(db):
    user = User.objects.create_user(username='empleado_demo', password='Pass123!')
    group = Group.objects.get(name='Empleado')
    user.groups.add(group)
    return user


@pytest.fixture
def catalogo_demo(db):
    categoria = Categoria.objects.create(nombre='Bebidas', descripcion='Productos de bebidas')
    proveedor = Proveedor.objects.create(
        nombre='Distribuidora Kiosco SRL',
        contacto='Ana Torres',
        telefono='351-1234567',
        email='ventas@distribuidorakiosco.com.ar',
        direccion='San Martín 1000',
        cuit='30-11223344-5',
    )
    producto = Producto.objects.create(
        nombre='Coca Cola 500ml',
        codigo_barra='779123456011',
        categoria=categoria,
        precio_venta=350.00,
        stock_actual=15,
        stock_minimo=5,
    )
    return {'categoria': categoria, 'proveedor': proveedor, 'producto': producto}


@pytest.mark.django_db
def test_login_page_accessible(client):
    response = client.get(reverse('login'))

    assert response.status_code == 200
    assert 'Iniciar sesión' in response.content.decode()


@pytest.mark.django_db
def test_login_correcto(client):
    User.objects.create_user(username='usuario1', password='Pass123!')

    response = client.post(reverse('login'), {'username': 'usuario1', 'password': 'Pass123!'})

    assert response.status_code == 302
    assert '_auth_user_id' in client.session


@pytest.mark.django_db
def test_login_incorrecto(client):
    response = client.post(reverse('login'), {'username': 'usuario_inesistente', 'password': 'bad-pass'})

    assert response.status_code == 200
    assert response.context['form'].errors


@pytest.mark.django_db
def test_logout(client, admin_user):
    client.force_login(admin_user)

    response = client.post(reverse('logout'))

    assert response.status_code == 302
    assert response.url == reverse('login')
    assert '_auth_user_id' not in client.session


@pytest.mark.django_db
def test_navbar_logout_form_present(client, admin_user):
    client.force_login(admin_user)
    response = client.get(reverse('home'))
    assert response.status_code == 200
    content = response.content.decode()
    assert f'action="{reverse("logout")}"' in content
    assert 'method="post"' in content


@pytest.mark.django_db
def test_private_pages_require_login(client):
    for name in ['home', 'catalogo:productos', 'catalogo:categorias', 'catalogo:proveedores']:
        response = client.get(reverse(name))
        assert response.status_code == 302
        assert response.url.startswith(reverse('login'))


@pytest.mark.django_db
def test_admin_puede_consultar_catalogo_y_ver_registros(client, admin_user, catalogo_demo):
    client.force_login(admin_user)
    assertions = [
        (reverse('home'), 'StockZ'),
        (reverse('catalogo:productos'), catalogo_demo['producto'].nombre),
        (reverse('catalogo:categorias'), catalogo_demo['categoria'].nombre),
        (reverse('catalogo:proveedores'), catalogo_demo['proveedor'].nombre),
    ]

    for url, expected in assertions:
        response = client.get(url)
        assert response.status_code == 200
        assert expected in response.content.decode()

    for url in [
        reverse('catalogo:producto_crear'),
        reverse('catalogo:categoria_crear'),
        reverse('catalogo:proveedor_crear'),
    ]:
        response = client.get(url)
        assert response.status_code == 200


@pytest.mark.django_db
def test_employee_puede_consultar_pero_no_crear(client, employee_user, catalogo_demo):
    client.force_login(employee_user)

    for url, expected in [
        (reverse('catalogo:productos'), catalogo_demo['producto'].nombre),
        (reverse('catalogo:categorias'), catalogo_demo['categoria'].nombre),
        (reverse('catalogo:proveedores'), catalogo_demo['proveedor'].nombre),
    ]:
        response = client.get(url)
        assert response.status_code == 200
        assert expected in response.content.decode()

    for url in [
        reverse('catalogo:producto_crear'),
        reverse('catalogo:categoria_crear'),
        reverse('catalogo:proveedor_crear'),
        reverse('catalogo:producto_editar', args=[catalogo_demo['producto'].pk]),
        reverse('catalogo:categoria_editar', args=[catalogo_demo['categoria'].pk]),
        reverse('catalogo:proveedor_editar', args=[catalogo_demo['proveedor'].pk]),
    ]:
        response = client.get(url)
        assert response.status_code == 403

    for url in [
        reverse('catalogo:producto_eliminar', args=[catalogo_demo['producto'].pk]),
        reverse('catalogo:categoria_eliminar', args=[catalogo_demo['categoria'].pk]),
        reverse('catalogo:proveedor_eliminar', args=[catalogo_demo['proveedor'].pk]),
    ]:
        response = client.post(url)
        assert response.status_code == 403


@pytest.mark.django_db
def test_admin_abm_productos(client, admin_user, catalogo_demo):
    client.force_login(admin_user)
    categoria = catalogo_demo['categoria']

    create_response = client.post(reverse('catalogo:producto_crear'), {
        'nombre': 'Galletas surtidas',
        'codigo_barra': '779000123456',
        'descripcion': 'Paquete de galletas',
        'categoria': categoria.pk,
        'precio_venta': '320.50',
        'stock_actual': '12',
        'stock_minimo': '3',
        'activo': 'on',
    })

    assert create_response.status_code == 302
    producto = Producto.objects.get(nombre='Galletas surtidas')

    edit_response = client.post(reverse('catalogo:producto_editar', args=[producto.pk]), {
        'nombre': 'Galletas surtidas premium',
        'codigo_barra': '779000123457',
        'descripcion': 'Paquete premium',
        'categoria': categoria.pk,
        'precio_venta': '250.10',
        'stock_actual': '8',
        'stock_minimo': '4',
        'activo': 'on',
    })

    assert edit_response.status_code == 302
    producto.refresh_from_db()
    assert producto.nombre == 'Galletas surtidas premium'
    assert producto.precio_venta == Decimal('250.10')

    delete_response = client.post(reverse('catalogo:producto_eliminar', args=[producto.pk]))
    assert delete_response.status_code == 302
    assert not Producto.objects.filter(pk=producto.pk).exists()


@pytest.mark.django_db
def test_admin_abm_categorias(client, admin_user):
    client.force_login(admin_user)

    create_response = client.post(reverse('catalogo:categoria_crear'), {
        'nombre': 'Lácteos',
        'descripcion': 'Productos lácteos',
        'activo': 'on',
    })

    assert create_response.status_code == 302
    categoria = Categoria.objects.get(nombre='Lácteos')

    edit_response = client.post(reverse('catalogo:categoria_editar', args=[categoria.pk]), {
        'nombre': 'Lacteos',
        'descripcion': 'Productos de leche y derivados',
        'activo': 'on',
    })

    assert edit_response.status_code == 302
    categoria.refresh_from_db()
    assert categoria.nombre == 'Lacteos'

    delete_response = client.post(reverse('catalogo:categoria_eliminar', args=[categoria.pk]))
    assert delete_response.status_code == 302
    assert not Categoria.objects.filter(pk=categoria.pk).exists()


@pytest.mark.django_db
def test_admin_abm_proveedores(client, admin_user):
    client.force_login(admin_user)

    create_response = client.post(reverse('catalogo:proveedor_crear'), {
        'nombre': 'Distribuidora Norte',
        'contacto': 'Lucas Pérez',
        'telefono': '351-2233445',
        'email': 'ventas@norte.com.ar',
        'direccion': 'Belgrano 700',
        'cuit': '30-99887766-1',
        'activo': 'on',
    })

    assert create_response.status_code == 302
    proveedor = Proveedor.objects.get(nombre='Distribuidora Norte')

    edit_response = client.post(reverse('catalogo:proveedor_editar', args=[proveedor.pk]), {
        'nombre': 'Distribuidora Norte SA',
        'contacto': 'Lucas Pérez',
        'telefono': '351-2233446',
        'email': 'norte@ventas.com.ar',
        'direccion': 'Belgrano 710',
        'cuit': '30-99887766-2',
        'activo': 'on',
    })

    assert edit_response.status_code == 302
    proveedor.refresh_from_db()
    assert proveedor.nombre == 'Distribuidora Norte SA'
    assert proveedor.email == 'norte@ventas.com.ar'

    delete_response = client.post(reverse('catalogo:proveedor_eliminar', args=[proveedor.pk]))
    assert delete_response.status_code == 302
    assert not Proveedor.objects.filter(pk=proveedor.pk).exists()


@pytest.mark.django_db
def test_validacion_de_datos_incorrectos(client, admin_user, catalogo_demo):
    client.force_login(admin_user)
    categoria = catalogo_demo['categoria']

    response = client.post(reverse('catalogo:producto_crear'), {
        'nombre': '',
        'codigo_barra': 'abc',
        'descripcion': 'Prueba',
        'categoria': categoria.pk,
        'precio_venta': '-1',
        'stock_actual': '-1',
        'stock_minimo': '-1',
    })
    assert response.status_code == 200
    assert response.context['form'].errors

    response = client.post(reverse('catalogo:categoria_crear'), {
        'nombre': '',
        'descripcion': '',
    })
    assert response.status_code == 200
    assert response.context['form'].errors

    response = client.post(reverse('catalogo:proveedor_crear'), {
        'nombre': 'Proveedor',
        'contacto': '',
        'telefono': '',
        'email': 'email-no-valido',
        'direccion': '',
        'cuit': '',
    })
    assert response.status_code == 200
    assert response.context['form'].errors


@pytest.mark.django_db
def test_home_muestra_rol_y_usuario(client, admin_user):
    client.force_login(admin_user)

    response = client.get(reverse('home'))

    assert response.status_code == 200
    assert 'StockZ' in response.content.decode()
    assert 'Administrador' in response.content.decode()
    assert 'admin_demo' in response.content.decode()

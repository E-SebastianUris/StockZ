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
    assert '_auth_user_id' not in client.session


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
def test_home_muestra_rol_y_usuario(client, admin_user):
    client.force_login(admin_user)

    response = client.get(reverse('home'))

    assert response.status_code == 200
    assert 'StockZ' in response.content.decode()
    assert 'Administrador' in response.content.decode()
    assert 'admin_demo' in response.content.decode()

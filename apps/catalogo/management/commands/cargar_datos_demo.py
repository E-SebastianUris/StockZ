from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from apps.catalogo.models import Categoria, Producto, Proveedor


class Command(BaseCommand):
    help = 'Carga datos ficticios de demostración para categorías, proveedores y productos.'

    @transaction.atomic
    def handle(self, *args, **options):
        categorias = {
            'Bebidas': 'Bebidas y refrescos para kiosco y consumo diario.',
            'Golosinas': 'Snacks, caramelos y dulces para venta minorista.',
            'Almacén': 'Productos básicos de almacén y hogar.',
            'Limpieza': 'Insumos de limpieza para el comercio y la casa.',
        }

        categoria_map = {}
        for nombre, descripcion in categorias.items():
            categoria, created = Categoria.objects.get_or_create(
                nombre=nombre,
                defaults={'descripcion': descripcion, 'activo': True},
            )
            if not created:
                categoria.descripcion = descripcion
                categoria.activo = True
                categoria.save(update_fields=['descripcion', 'activo', 'actualizado_el'])
            categoria_map[nombre] = categoria

        proveedores = [
            {
                'nombre': 'Distribuidora del Sur S.A.',
                'contacto': 'María López',
                'telefono': '351-4567890',
                'email': 'ventas@distribuidorasur.com.ar',
                'direccion': 'Av. San Martín 1234, Córdoba',
                'cuit': '30-12345678-1',
            },
            {
                'nombre': 'Kiosco Premium',
                'contacto': 'Carlos Gómez',
                'telefono': '341-2345678',
                'email': 'compras@kioscopremium.com.ar',
                'direccion': 'Calle Belgrano 890, Rosario',
                'cuit': '30-23456789-2',
            },
            {
                'nombre': 'Aroma & Limpieza SRL',
                'contacto': 'Lucía Pérez',
                'telefono': '112-3344556',
                'email': 'contacto@aromalimpieza.com.ar',
                'direccion': 'Ruta 9 km 42, La Plata',
                'cuit': '30-34567890-3',
            },
        ]

        proveedor_map = {}
        for proveedor_data in proveedores:
            proveedor, created = Proveedor.objects.get_or_create(
                cuit=proveedor_data['cuit'],
                defaults={
                    'nombre': proveedor_data['nombre'],
                    'contacto': proveedor_data['contacto'],
                    'telefono': proveedor_data['telefono'],
                    'email': proveedor_data['email'],
                    'direccion': proveedor_data['direccion'],
                    'activo': True,
                },
            )
            if not created:
                for field, value in proveedor_data.items():
                    if field == 'cuit':
                        continue
                    setattr(proveedor, field, value)
                proveedor.activo = True
                proveedor.save()
            proveedor_map[proveedor_data['nombre']] = proveedor

        productos = [
            {
                'nombre': 'Coca Cola 500ml',
                'codigo_barra': '779123456001',
                'descripcion': 'Gaseosa clásica de 500 ml.',
                'categoria': 'Bebidas',
                'precio_venta': Decimal('350.00'),
                'stock_actual': 40,
                'stock_minimo': 10,
            },
            {
                'nombre': 'Agua Mineral 1.5L',
                'codigo_barra': '779123456002',
                'descripcion': 'Agua mineral sin gas.',
                'categoria': 'Bebidas',
                'precio_venta': Decimal('260.00'),
                'stock_actual': 25,
                'stock_minimo': 8,
            },
            {
                'nombre': 'Galletitas Oreo',
                'codigo_barra': '779123456003',
                'descripcion': 'Paquete de galletitas de chocolate.',
                'categoria': 'Golosinas',
                'precio_venta': Decimal('420.00'),
                'stock_actual': 30,
                'stock_minimo': 12,
            },
            {
                'nombre': 'Chicles Mentos',
                'codigo_barra': '779123456004',
                'descripcion': 'Chicles de menta en caja.',
                'categoria': 'Golosinas',
                'precio_venta': Decimal('180.00'),
                'stock_actual': 55,
                'stock_minimo': 15,
            },
            {
                'nombre': 'Caramelos Sugus',
                'codigo_barra': '779123456005',
                'descripcion': 'Paquete surtido de caramelos.',
                'categoria': 'Golosinas',
                'precio_venta': Decimal('200.00'),
                'stock_actual': 48,
                'stock_minimo': 10,
            },
            {
                'nombre': 'Arroz 1kg',
                'codigo_barra': '779123456006',
                'descripcion': 'Arroz blanco de uso doméstico.',
                'categoria': 'Almacén',
                'precio_venta': Decimal('520.00'),
                'stock_actual': 20,
                'stock_minimo': 6,
            },
            {
                'nombre': 'Fideos Spaghetti 500g',
                'codigo_barra': '779123456007',
                'descripcion': 'Fideos secos para cocina familiar.',
                'categoria': 'Almacén',
                'precio_venta': Decimal('310.00'),
                'stock_actual': 24,
                'stock_minimo': 7,
            },
            {
                'nombre': 'Lavandina 1L',
                'codigo_barra': '779123456008',
                'descripcion': 'Lavadina para limpieza del hogar.',
                'categoria': 'Limpieza',
                'precio_venta': Decimal('280.00'),
                'stock_actual': 18,
                'stock_minimo': 8,
            },
            {
                'nombre': 'Detergente 1L',
                'codigo_barra': '779123456009',
                'descripcion': 'Detergente líquido para ropa.',
                'categoria': 'Limpieza',
                'precio_venta': Decimal('360.00'),
                'stock_actual': 22,
                'stock_minimo': 9,
            },
            {
                'nombre': 'Papel Higiénico x4',
                'codigo_barra': '779123456010',
                'descripcion': 'Pack de papel higiénico de 4 unidades.',
                'categoria': 'Limpieza',
                'precio_venta': Decimal('510.00'),
                'stock_actual': 16,
                'stock_minimo': 5,
            },
        ]

        created_count = 0
        for producto_data in productos:
            producto, created = Producto.objects.get_or_create(
                codigo_barra=producto_data['codigo_barra'],
                defaults={
                    'nombre': producto_data['nombre'],
                    'descripcion': producto_data['descripcion'],
                    'categoria': categoria_map[producto_data['categoria']],
                    'precio_venta': producto_data['precio_venta'],
                    'stock_actual': producto_data['stock_actual'],
                    'stock_minimo': producto_data['stock_minimo'],
                    'activo': True,
                },
            )
            if created:
                created_count += 1
            else:
                producto.nombre = producto_data['nombre']
                producto.descripcion = producto_data['descripcion']
                producto.categoria = categoria_map[producto_data['categoria']]
                producto.precio_venta = producto_data['precio_venta']
                producto.stock_actual = producto_data['stock_actual']
                producto.stock_minimo = producto_data['stock_minimo']
                producto.activo = True
                producto.save()

        categoria_total = Categoria.objects.count()
        proveedor_total = Proveedor.objects.count()
        producto_total = Producto.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Carga demo completada. Categorías: {categoria_total}, Proveedores: {proveedor_total}, Productos: {producto_total}. '
                f'Productos creados en esta ejecución: {created_count}.'
            )
        )

from django.db import models


class Categoria(models.Model):
    """Categoría del catálogo. Base reutilizada de StockX adaptada al alcance de StockZ."""

    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, default='')
    activo = models.BooleanField(default=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre


class Proveedor(models.Model):
    """Proveedor de insumos o productos. Se modela sin la relación de compra histórica de StockX."""

    nombre = models.CharField(max_length=150)
    contacto = models.CharField(max_length=100, blank=True, default='')
    telefono = models.CharField(max_length=30, blank=True, default='')
    email = models.EmailField(blank=True, default='')
    direccion = models.CharField(max_length=255, blank=True, default='')
    cuit = models.CharField(max_length=20, unique=True, blank=True, default='')
    activo = models.BooleanField(default=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    """Producto del catálogo. Se excluyen elementos de compra/stock avanzados y de ventas."""

    nombre = models.CharField(max_length=150)
    codigo_barra = models.CharField(max_length=64, unique=True, blank=True, default='')
    descripcion = models.TextField(blank=True, default='')
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT, related_name='productos')
    precio_venta = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    stock_actual = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)
    creado_el = models.DateTimeField(auto_now_add=True)
    actualizado_el = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        constraints = [
            models.CheckConstraint(check=models.Q(precio_venta__gte=0), name='stockz_producto_precio_venta_gte_0'),
            models.CheckConstraint(check=models.Q(stock_actual__gte=0), name='stockz_producto_stock_actual_gte_0'),
            models.CheckConstraint(check=models.Q(stock_minimo__gte=0), name='stockz_producto_stock_minimo_gte_0'),
        ]

    def __str__(self):
        return self.nombre

from django import forms

from .models import Categoria, Producto, Proveedor


class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['nombre', 'descripcion', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre


class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'direccion', 'cuit', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'cuit': forms.TextInput(attrs={'class': 'form-control'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre

    def clean_email(self):
        email = (self.cleaned_data.get('email') or '').strip()
        if email and '@' not in email:
            raise forms.ValidationError('El email no tiene un formato válido.')
        return email

    def clean_telefono(self):
        telefono = (self.cleaned_data.get('telefono') or '').strip()
        if telefono and len(telefono) < 6:
            raise forms.ValidationError('El teléfono debe tener al menos 6 caracteres.')
        return telefono

    def clean_cuit(self):
        cuit = (self.cleaned_data.get('cuit') or '').strip()
        if cuit and len(cuit) < 11:
            raise forms.ValidationError('El CUIT debe tener un formato válido.')
        return cuit


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'codigo_barra', 'descripcion', 'categoria', 'precio_venta', 'stock_actual', 'stock_minimo', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'codigo_barra': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'min': '0'}),
            'stock_actual': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'min': '0', 'step': '1'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_nombre(self):
        nombre = (self.cleaned_data.get('nombre') or '').strip()
        if not nombre:
            raise forms.ValidationError('El nombre es obligatorio.')
        return nombre

    def clean_codigo_barra(self):
        codigo_barra = (self.cleaned_data.get('codigo_barra') or '').strip()
        if codigo_barra and not codigo_barra.isdigit():
            raise forms.ValidationError('El código de barras debe contener solo números.')
        return codigo_barra

    def clean_precio_venta(self):
        precio = self.cleaned_data.get('precio_venta')
        if precio is not None and precio < 0:
            raise forms.ValidationError('El precio de venta no puede ser negativo.')
        return precio

    def clean_stock_actual(self):
        stock_actual = self.cleaned_data.get('stock_actual')
        if stock_actual is not None and stock_actual < 0:
            raise forms.ValidationError('El stock actual no puede ser negativo.')
        return stock_actual

    def clean_stock_minimo(self):
        stock_minimo = self.cleaned_data.get('stock_minimo')
        if stock_minimo is not None and stock_minimo < 0:
            raise forms.ValidationError('El stock mínimo no puede ser negativo.')
        return stock_minimo

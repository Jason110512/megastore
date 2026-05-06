from django import forms
from .models import Producto, Categoria, Orden


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'precio', 'precio_original',
            'stock', 'categoria', 'imagen', 'imagen2', 'imagen3', 'imagen4',
            'estrellas', 'num_resenas', 'colores', 'tallas',
            'envio_gratis', 'meses_sin_intereses', 'disponible'
        ]
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Escribe el nombre...'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Descripción del producto...'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '$0.00', 'step': '0.01'}),
            'precio_original': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio antes de descuento (opcional)', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad de inventario'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'imagen': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.webp'}),
            'imagen2': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.webp'}),
            'imagen3': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.webp'}),
            'imagen4': forms.FileInput(attrs={'class': 'form-control', 'accept': '.jpg,.jpeg,.png,.webp'}),
            'estrellas': forms.Select(attrs={'class': 'form-select'}),
            'num_resenas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'colores': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Blanco,Negro,Rosa,Azul'}),
            'tallas': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'XS,S,M,L,XL o 38,39,40'}),
            'envio_gratis': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'meses_sin_intereses': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'disponible': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_disponible(self):
        # Fix: asegurar que disponible se procese correctamente
        return self.cleaned_data.get('disponible', False)


class EnvioForm(forms.ModelForm):
    numero_tarjeta = forms.CharField(required=False, max_length=19,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '1234 5678 9012 3456', 'maxlength': '19'}))
    nombre_tarjeta = forms.CharField(required=False, max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre en la tarjeta'}))
    expiracion = forms.CharField(required=False, max_length=5,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/AA', 'maxlength': '5'}))
    cvv = forms.CharField(required=False, max_length=4,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '•••', 'type': 'password', 'maxlength': '4'}))
    banco_origen = forms.CharField(required=False, max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de tu banco'}))
    referencia_transferencia = forms.CharField(required=False, max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Número de referencia'}))

    class Meta:
        model = Orden
        fields = ['nombre_envio', 'direccion', 'ciudad', 'estado_envio', 'codigo_postal', 'metodo_pago']
        widgets = {
            'nombre_envio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre Completo'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ciudad'}),
            'estado_envio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Estado'}),
            'codigo_postal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código Postal'}),
            'metodo_pago': forms.Select(
                choices=[
                    ('Tarjeta de Crédito', 'Tarjeta de Crédito'),
                    ('Transferencia', 'Transferencia'),
                    ('Efectivo', 'Efectivo'),
                ],
                attrs={'class': 'form-select', 'onchange': 'togglePago(this.value)'}
            ),
        }

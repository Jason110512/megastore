from django.db import models
from accounts.models import Usuario


class Categoria(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Categorias'

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    precio_original = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,
        help_text='Precio antes de descuento (opcional)')
    stock = models.IntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, blank=True)
    imagen = models.ImageField(upload_to='productos/', blank=True, null=True)
    imagen2 = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name='Imagen 2')
    imagen3 = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name='Imagen 3')
    imagen4 = models.ImageField(upload_to='productos/', blank=True, null=True, verbose_name='Imagen 4')
    estrellas = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    num_resenas = models.IntegerField(default=0, verbose_name='Número de reseñas')
    disponible = models.BooleanField(default=True)
    colores = models.CharField(max_length=300, blank=True,
        help_text='Colores separados por coma: Blanco,Negro,Rosa,Azul')
    tallas = models.CharField(max_length=300, blank=True,
        help_text='Tallas separadas por coma: XS,S,M,L,XL o 38,39,40,41')
    envio_gratis = models.BooleanField(default=False, verbose_name='Envío gratis')
    meses_sin_intereses = models.IntegerField(default=0,
        help_text='Número de meses sin intereses (0 = no aplica)')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

    def pocas_piezas(self):
        return self.stock > 0 and self.stock < 10

    def get_colores(self):
        if self.colores:
            return [c.strip() for c in self.colores.split(',') if c.strip()]
        return []

    def get_tallas(self):
        if self.tallas:
            return [t.strip() for t in self.tallas.split(',') if t.strip()]
        return []

    def get_imagenes(self):
        imgs = []
        if self.imagen:
            imgs.append(self.imagen.url)
        if self.imagen2:
            imgs.append(self.imagen2.url)
        if self.imagen3:
            imgs.append(self.imagen3.url)
        if self.imagen4:
            imgs.append(self.imagen4.url)
        return imgs

    def descuento_porcentaje(self):
        if self.precio_original and self.precio_original > self.precio:
            diff = self.precio_original - self.precio
            return int((diff / self.precio_original) * 100)
        return 0


class Orden(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('enviado', 'Enviado'),
        ('entregado', 'Entregado'),
        ('cancelado', 'Cancelado'),
    )
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    nombre_envio = models.CharField(max_length=150, blank=True)
    direccion = models.CharField(max_length=300, blank=True)
    ciudad = models.CharField(max_length=100, blank=True)
    estado_envio = models.CharField(max_length=100, blank=True)
    codigo_postal = models.CharField(max_length=10, blank=True)
    metodo_pago = models.CharField(max_length=50, default='Tarjeta de Crédito')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    costo_envio = models.DecimalField(max_digits=10, decimal_places=2, default=100)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Orden #{self.id} - {self.usuario.username}"

    def calcular_total(self):
        self.subtotal = sum(item.subtotal() for item in self.items.all())
        self.total = self.subtotal + self.costo_envio
        self.save()


class OrdenItem(models.Model):
    orden = models.ForeignKey(Orden, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"


class Carrito(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def total(self):
        return sum(item.subtotal() for item in self.items.all())

    def total_items(self):
        return sum(item.cantidad for item in self.items.all())

    def __str__(self):
        return f"Carrito de {self.usuario.username}"


class CarritoItem(models.Model):
    carrito = models.ForeignKey(Carrito, related_name='items', on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)

    def subtotal(self):
        return self.cantidad * self.producto.precio

    def __str__(self):
        return f"{self.cantidad}x {self.producto.nombre}"


class Factura(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.numero}"

    def save(self, *args, **kwargs):
        if not self.numero:
            last = Factura.objects.order_by('-id').first()
            num = (last.id + 1) if last else 1
            self.numero = f"FAC-{num:05d}"
        super().save(*args, **kwargs)

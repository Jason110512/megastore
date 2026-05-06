from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    ROLES = (
        ('cliente', 'Cliente'),
        ('admin', 'Administrador'),
    )
    nombre_completo = models.CharField(max_length=150, blank=True)
    correo = models.EmailField(unique=True, blank=True, null=True)
    rol = models.CharField(max_length=10, choices=ROLES, default='cliente')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.rol})"

    def is_admin_store(self):
        return self.rol == 'admin' or self.is_staff

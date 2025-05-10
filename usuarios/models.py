# usuarios/models.py
from django.db import models
from django.contrib.auth.models import User

class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    foto = models.ImageField(upload_to='empleados/fotos/', null=True, blank=True)
    cargo = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.nombre

class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    NIT = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=255)
    telefono = models.CharField(max_length=20)
    nombre_contacto = models.CharField(max_length=150)
    sede = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    id_tipo = models.ForeignKey("ordenes.TipoEmpresa", on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nombre} - {self.NIT}"

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('trabajador', 'Trabajador'),
    )
    
    role = models.CharField(max_length=20, choices=ROLES, default='trabajador')
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    direccion = models.TextField()
    fecha_registro = models.DateTimeField(auto_now_add=True)

class FormatoFumigacion(models.Model):
    ESTADOS = (
        ('pendiente', 'Pendiente'),
        ('revisado', 'Revisado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    
    trabajador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='formatos')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_servicio = models.DateTimeField()
    tipo_servicio = models.CharField(max_length=100)
    observaciones = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

class Agenda(models.Model):
    trabajador = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='agendas')
    formato = models.ForeignKey(FormatoFumigacion, on_delete=models.CASCADE)
    fecha = models.DateTimeField()
    estado = models.CharField(max_length=20, choices=(
        ('programado', 'Programado'),
        ('en_proceso', 'En Proceso'),
        ('completado', 'Completado'),
        ('cancelado', 'Cancelado'),
    ), default='programado')

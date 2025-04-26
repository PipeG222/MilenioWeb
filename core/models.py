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
    
    def __str__(self):
        return self.nombre

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
    
    def __str__(self):
        return f"Servicio para {self.cliente.nombre} - {self.tipo_servicio}"

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
    
    def __str__(self):
        return f"Agenda para {self.formato.cliente.nombre} - {self.fecha}"

class SolicitudCita(models.Model):
    ESTADOS_SOLICITUD = (
        ('pendiente', 'Pendiente'),
        ('contactado', 'Contactado'),
        ('agendado', 'Agendado'),
        ('cancelado', 'Cancelado'),
    )
    
    TIPOS_SERVICIO = (
        ('fumigacion_general', 'Fumigación General'),
        ('control_plagas', 'Control de Plagas'),
        ('desinfeccion', 'Desinfección'),
        ('control_termitas', 'Control de Termitas'),
        ('control_roedores', 'Control de Roedores'),
        ('otro', 'Otro'),
    )
    
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    email = models.EmailField()
    direccion = models.TextField()
    tipo_servicio = models.CharField(max_length=50, choices=TIPOS_SERVICIO)
    mensaje = models.TextField()
    fecha_preferencia = models.DateField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS_SOLICITUD, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Solicitud de {self.nombre} - {self.get_tipo_servicio_display()}"

from django.db import models

# Create your models here.

class Usuario(models.Model):
    correo = models.EmailField(unique=True)
    nombre = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    idDevice = models.CharField(max_length=255, blank=True, null=True)
    aprobado = models.BooleanField(default=False)

    def __str__(self):
        return self.nombre

class Empleado(models.Model):
    nombre = models.CharField(max_length=255)
    foto = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class TipoInsecto(models.Model):
    descripcion = models.CharField(max_length=255)
    abreviado = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.descripcion

class Insecto(models.Model):
    descripcion = models.CharField(max_length=255)
    tipo_insecto = models.ForeignKey(TipoInsecto, on_delete=models.CASCADE)

    def __str__(self):
        return self.descripcion

class Orden(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    fecha_inicio = models.DateField()
    fecha_usuario = models.DateField()
    idTipoCliente = models.IntegerField(blank=True, null=True)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    serial = models.CharField(max_length=255, blank=True, null=True)
    operario = models.BooleanField(default=False)
    hora_ingreso = models.TimeField(blank=True, null=True)
    hora_salida = models.TimeField(blank=True, null=True)
    observaciones_tecnicas = models.TextField(blank=True, null=True)
    correctivos = models.TextField(blank=True, null=True)
    firma_operario_tecnico = models.TextField(blank=True, null=True)
    firma_ayudante = models.TextField(blank=True, null=True)
    tipo_servicio = models.CharField(max_length=255, blank=True, null=True)
    objetivo_del_servicio = models.TextField(blank=True, null=True)
    estado_envio = models.CharField(max_length=255, blank=True, null=True)
    tipo_orden = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Orden {self.id} - {self.usuario.nombre}"

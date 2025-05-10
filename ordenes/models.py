from django.db import models
from usuarios.models import Cliente, Empleado

# Tipos de empresa: Simple o Compleja
class TipoEmpresa(models.Model):
    nombre = models.CharField(max_length=100)  # Ejemplo: "Simple", "Compleja"

    def __str__(self):
        return self.nombre

# Orden principal
class Orden(models.Model):
    TIPO_ORDEN_CHOICES = [
        ('INSPECCION', 'Inspección General'),
        ('BENEFICIO', 'Inspección Planta Beneficio'),
    ]

    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('finalizada', 'Finalizada'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    trabajadores = models.ManyToManyField(Empleado)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tipo = models.CharField(max_length=50, choices=TIPO_ORDEN_CHOICES)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')

    def __str__(self):
        return f"Orden #{self.id} - {self.get_tipo_display()}"

# Subformulario: Inspección General
class InspeccionGeneral(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    especie_encontrada = models.TextField()
    evidencias = models.TextField()
    hallazgos_planta = models.TextField()
    uso_plaguicidas = models.TextField()
    observaciones = models.TextField(blank=True)
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True)
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True)
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Inspección de Orden #{self.orden.id}"

# Subformulario: Orden Locativos
class OrdenLocativos(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    tipo_servicio = models.CharField(max_length=50)
    lugares = models.TextField()
    areas = models.TextField()
    materiales = models.TextField()
    observaciones = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True)
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True)
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Locativos de Orden #{self.orden.id}"

# Subformulario: Desinfección de Ambientes
class DesinfeccionAmbientes(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    hallazgos = models.TextField()
    zonas_servicio = models.TextField()
    ingredientes = models.TextField()
    observaciones = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True)
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True)
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Desinfección de Orden #{self.orden.id}"

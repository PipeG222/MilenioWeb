from django.db import models
from usuarios.models import Cliente, Empleado
from django.utils.translation import gettext_lazy as _
# Tipos de empresa: Simple o Compleja
class TipoEmpresa(models.Model):
    nombre = models.CharField(max_length=100)  

    def __str__(self):
        return self.nombre

# Orden principal
class Orden(models.Model):
    TIPO_ORDEN_CHOICES = [
        ('ORDEN_SERVICIO', 'Orden de Servicio'),
        ('INSPECCION', 'Inspección General'),
        ('SACRIFICIO', 'Inspección Planta Sacrificio'),
        ('SERVICIOS_LOCATIVOS', 'Servicios Locativos'),
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
    
    class Meta:
        verbose_name = _("Orden")
        verbose_name_plural = _("Órdenes")

# Subformulario: Inspección General

class Zona(models.Model):
    """
    Definición global de una zona (p.ej. Cocina, Sala).
    Se reutiliza entre órdenes y se asocia a uno o varios tipos de empresa.
    """
    nombre = models.CharField(max_length=50, unique=True)
    tipos_empresa = models.ManyToManyField(
        'TipoEmpresa',
        related_name='zonas'
    )

    class Meta:
        verbose_name = _("Zona")
        verbose_name_plural = _("Zonas")

    def __str__(self):
        return self.nombre

class Area(models.Model):
    """
    Definición global de un área dentro de una zona (p.ej. Cielo raso, Alacena).
    """
    zona = models.ForeignKey(
        Zona,
        related_name='areas',
        on_delete=models.CASCADE
    )
    nombre = models.CharField(max_length=50)

    class Meta:
        unique_together = ('zona', 'nombre')
        verbose_name = _("Área")
        verbose_name_plural = _("Áreas")

    def __str__(self):
        return f"{self.nombre} ({self.zona.nombre})"

class OrdenLocativos(models.Model):

    class Meta:
        verbose_name = _("Orden Locativo")
        verbose_name_plural = _("Órdenes Locativos")

    orden = models.OneToOneField(
        'Orden',
        on_delete=models.CASCADE,
        related_name='locativo'
    )
    TIPO_SERVICIO_CHOICES = [
        ('INSTALACION', 'Instalación'),
        ('ARREGLO_LOCATIVO', 'Arreglo locativo'),
    ]
    tipo_servicio = models.CharField(
        max_length=20,
        choices=TIPO_SERVICIO_CHOICES
    )
    especies = models.ManyToManyField(
        'Plaga',
        blank=True,
        related_name='ordenes_locativas'
    )

    zonas = models.ManyToManyField(
        Zona,
        through='OrdenLocativoZona',
        related_name='ordenes_locativos'
    )
    observaciones = models.TextField(blank=True)
    recomendaciones = models.TextField(blank=True)
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True)
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True)
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Locativos de Orden #{self.orden.id}"

class OrdenLocativoZona(models.Model):
    """
    Asociación de una orden locativa con una zona global.
    """

    orden_locativo = models.ForeignKey(
        OrdenLocativos,
        related_name='orden_zonas',
        on_delete=models.CASCADE
    )
    zona = models.ForeignKey(
        Zona,
        related_name='orden_zonas',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('orden_locativo', 'zona')
        verbose_name = _("Orden Locativo Zona")
        verbose_name_plural = _("Órdenes Locativos Zonas")

    def __str__(self):
        return f"Orden {self.orden_locativo.orden.id} - Zona {self.zona.nombre}"

class OrdenLocativoArea(models.Model):
    """
    Selección de áreas específicas dentro de una Zona para una orden locativa.
    """
        


    orden_zona = models.ForeignKey(
        OrdenLocativoZona,
        related_name='orden_areas',
        on_delete=models.CASCADE
    )
    
    area = models.ForeignKey(
        Area,
        related_name='orden_areas',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('orden_zona', 'area')
        verbose_name = _("Orden Locativo Área")
        verbose_name_plural = _("Órdenes Locativos Áreas")

    def __str__(self):
        return f"Orden {self.orden_zona.orden_locativo.orden.id} - Area {self.area.nombre}"

# Materiales y uso de materiales
class Material(models.Model):
    """
    Catálogo global de materiales (p.ej. Alambre) y su unidad de medida.
    """
    nombre = models.CharField(max_length=100, unique=True)
    unidad_medida = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nombre} ({self.unidad_medida})"
    
    class Meta:
        verbose_name = _("Material")
        verbose_name_plural = _("Materiales")

# Modelo para categorías de plagas
class CategoriaPlagas(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    
    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = _("Categoría de Plaga")
        verbose_name_plural = _("Categorías de Plagas")
        ordering = ['nombre']

# Modelo para especies de plagas
class Plaga(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    categoria = models.ForeignKey(
        CategoriaPlagas, 
        on_delete=models.CASCADE, 
        related_name='especies'
    )
    descripcion = models.TextField(blank=True)
    nivel_riesgo = models.CharField(
        max_length=20, 
        choices=[
            ('BAJO', 'Bajo'),
            ('MEDIO', 'Medio'),
            ('ALTO', 'Alto'),
        ],
        default='MEDIO'
    )
    habitat_comun = models.TextField(blank=True)
    metodo_control = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='plagas/', blank=True, null=True)
    activa = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.categoria.nombre})"
    
    class Meta:
        verbose_name = _("Plaga")
        verbose_name_plural = _("Plagas")
        ordering = ['categoria', 'nombre']

class MaterialUso(models.Model):
    """
    Registro de cantidad utilizada de cada material en una orden locativa.
    """
    orden_locativo = models.ForeignKey(
        OrdenLocativos,
        related_name='materiales_usados',
        on_delete=models.CASCADE
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.PROTECT
    )
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cantidad} {self.material.unidad_medida} de {self.material.nombre}"

    class Meta:
        verbose_name = _("Material Uso")
        verbose_name_plural = _("Materiales Usados")

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
    
    class Meta:
        verbose_name = _("Desinfección de Ambientes")
        verbose_name_plural = _("Desinfecciones de Ambientes")

class InspeccionGeneral(models.Model):
    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    especies_encontradas = models.ManyToManyField(
        Plaga, 
        related_name='inspecciones',
        blank=True,
        verbose_name=_("Especies encontradas")
    )
    evidencias = models.TextField()
    hallazgos_planta = models.TextField()
    uso_plaguicidas = models.TextField()
    observaciones = models.TextField(blank=True)
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True)
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True)
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True)

    def __str__(self):
        return f"Inspección de Orden #{self.orden.id}"
    
    class Meta:
        verbose_name = _("Inspección General")
        verbose_name_plural = _("Inspecciones Generales")

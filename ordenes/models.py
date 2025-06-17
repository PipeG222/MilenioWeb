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
# class AspectoLocativoHigiene(models.Model):
#     class RespuestaChoices(models.TextChoices):
#         SI = 'SI', _('Sí')
#         NO = 'NO', _('No')
#         NO_APLICA = 'NA', _('No Aplica')

#     orden = models.OneToOneField(Orden, on_delete=models.CASCADE, related_name='aspecto_locativo_higiene')
#     vias_acceso_cerradas = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Vías de acceso bien cerradas')
#     paredes_sin_grietas = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Estado de paredes sin grietas')
#     condiciones_orden_aseo = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Buenas condiciones de orden y aseo')
#     basuras_con_tapa = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Basuras con tapa y evacuadas permanentemente')
#     luz_puertas_menor_1cm = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Luz en puertas menor a 1 cm')
#     techos_buen_estado = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Techos en buen estado')
#     pisos_media_cana_sin_grieta = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Pisos con media caña y sin grieta')
#     ventana_proteccion_malla = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Ventana con protección malla')
#     presencia_grasa = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Presencia de grasa')
#     manejo_basuras_adecuado = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Manejo de basuras adecuado')
#     exteriores_limpios_sin_basura = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Exteriores limpios sin basuras y adecuado control de maleza')
#     estibacion_conserva_espacio = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='La estibación: conserva espacio contra la pared y permite las labores de aseo y control de plagas')
#     rejillas_desague_pisos = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Rejillas: para correcto desague de pisos')
#     paredes_pisos_limpios = models.CharField(max_length=2, choices=RespuestaChoices.choices, default=RespuestaChoices.NO_APLICA, verbose_name='Paredes y pisos limpios y buenos')

#     def __str__(self):
#         return f"Aspecto Locativo e Higiene de Orden #{self.orden.id}"

#     class Meta:
#         verbose_name = _("Aspecto Locativo e Higiene")
#         verbose_name_plural = _("Aspectos Locativos e Higiene")


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

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name=_("Sección / Categoría"))
    descripcion = models.TextField(blank=True,
            null=True,
            help_text="(opcional) Descripción breve de la sección")

    class Meta:
        verbose_name = _("Sección / Categoría")
        verbose_name_plural = _("Secciones / Categorías")


class ItemCategoria(models.Model):
    categoria = models.ForeignKey('Categoria', on_delete=models.CASCADE, related_name='items', verbose_name=_("Sección / Categoría"))
    nombre = models.CharField(max_length=100, verbose_name=_("Nombre del Item"))
        
    boolean_choices = (
        ("SI", "SI"),
        ("NO", "NO"),
        ("NA", "N/A")
    )
    respuesta = models.CharField(max_length=3, choices=boolean_choices, verbose_name=_("Respuesta"))

    def __str__(self):
        return f"{self.nombre} - {self.get_respuesta_display()}"


class TipoServicio(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("Tipo de Servicio")
        verbose_name_plural = _("Tipos de Servicio")

    def __str__(self):
        return self.nombre


class Higiene(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("Higiene")
        verbose_name_plural = _("Higienes")

    def __str__(self):
        return self.nombre


class AreaLocativa(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = _("Área Locativa")
        verbose_name_plural = _("Áreas Locativas")

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    ingrediente_activo = models.CharField(max_length=200)
    dosificacion = models.CharField(max_length=100)
    fecha_vencimiento = models.DateField()
    ultimo_lote = models.CharField(max_length=100)

    class Meta:
        verbose_name = _("Producto")
        verbose_name_plural = _("Productos")

    def __str__(self):
        return self.nombre


class OrdenServicio(models.Model):
    orden_principal = models.ForeignKey(
        Orden,
        on_delete=models.CASCADE,
        related_name='servicios'
    )
    tipo = models.ForeignKey(
        TipoServicio,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_("Tipo de Servicio")
    )
    numero_control = models.PositiveIntegerField(editable=False)
    fechadelservicio = models.DateTimeField(editable=False)
    especies = models.ManyToManyField(
        Plaga,
        blank=True,
        related_name='ordenes_servicio',
        verbose_name=_("Especies")
    )
    higiene = models.ForeignKey(
        Higiene,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Higiene")
    )
    areaslocativas = models.ManyToManyField(
        AreaLocativa,
        blank=True,
        related_name='ordenes_servicio',
        verbose_name=_("Áreas Locativas")
    )
    zonas = models.ManyToManyField(
        Zona,
        through='OrdenServicioZona',
        related_name='ordenes_servicio',
        verbose_name=_("Zonas")
    )
    productos = models.ManyToManyField(
        Producto,
        blank=True,
        related_name='ordenes_servicio',
        verbose_name=_("Productos")
    )
    observaciones = models.TextField(blank=True, verbose_name=_("Observaciones"))
    recomendaciones = models.TextField(blank=True, verbose_name=_("Recomendaciones"))
    firma_operario = models.ImageField(upload_to='firmas/', blank=True, null=True, verbose_name=_("Firma Operario"))
    firma_acompanante = models.ImageField(upload_to='firmas/', blank=True, null=True, verbose_name=_("Firma Acompañante"))
    certificado = models.FileField(upload_to='certificados/', blank=True, null=True, verbose_name=_("Certificado"))

    class Meta:
        verbose_name = _("Orden de Servicio")
        verbose_name_plural = _("Órdenes de Servicio")
        unique_together = [['orden_principal', 'numero_control']]

    def save(self, *args, **kwargs):
        # Set fecha del servicio from the principal order
        if not self.fechadelservicio:
            self.fechadelservicio = self.orden_principal.fecha_creacion

        # Incremental numero_control per client
        if not self.numero_control:
            cliente = self.orden_principal.cliente
            ultima = (
                OrdenServicio.objects
                .filter(orden_principal__cliente=cliente)
                .aggregate(models.Max('numero_control'))
                ['numero_control__max']
                or 0
            )
            self.numero_control = ultima + 1

        super().save(*args, **kwargs)


class OrdenServicioZona(models.Model):
    orden_servicio = models.ForeignKey(
        OrdenServicio,
        on_delete=models.CASCADE,
        related_name='zonas_servicio'
    )
    zona = models.ForeignKey(
        Zona,
        on_delete=models.CASCADE,
        related_name='zonas_servicio'
    )

    class Meta:
        verbose_name = _("Zona en Orden de Servicio")
        verbose_name_plural = _("Zonas en Órdenes de Servicio")
        unique_together = [['orden_servicio', 'zona']]

    def __str__(self):
        return f"{self.zona} en {self.orden_servicio}"

# Ejemplo de uso de MaterialUso existente:
# mat = Material.objects.get(pk=mid_int)
# MaterialUso.objects.create(
#     orden_servicio=orden_servicio_obj,
#     material=mat,
#     cantidad=cantidad
# )
class HigieneUso(models.Model):
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE)
    higiene       = models.ForeignKey(Higiene, on_delete=models.CASCADE)
    nivel         = models.CharField(max_length=10, choices=[('alto','Alto'),('medio','Medio'),('bajo','Bajo')])

class EspecieUso(models.Model):
    orden_servicio = models.ForeignKey(OrdenServicio, on_delete=models.CASCADE)
    plaga          = models.ForeignKey(Plaga, on_delete=models.CASCADE)
    nivel          = models.CharField(max_length=10, choices=[('alto','Alto'),('medio','Medio'),('bajo','Bajo')])

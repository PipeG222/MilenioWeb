from traceback import format_tb
from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.html import format_html
from .models import (
    TipoEmpresa,
    Orden,
    InspeccionGeneral,
    DesinfeccionAmbientes,
    Zona,
    Area,
    Material,
    OrdenLocativos,
    CategoriaPlagas,
    Plaga,
)



@admin.register(OrdenLocativos)
class OrdenLocativosAdmin(admin.ModelAdmin):
    # Muestra el id de la orden (a través de la relación OneToOne),
    # el tipo de servicio y luego los botones de editar / eliminar
    list_display = ('orden', 'tipo_servicio', 'editar_link', 'eliminar_link')

    def add_view(self, request, form_url='', extra_context=None):
        return redirect(reverse('ordenes:ordenlocativos_add'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return redirect(reverse('ordenes:ordenlocativos_change', args=[object_id]))

    # Link “Editar” hacia tu vista personalizada de change
    def editar_link(self, obj):
        url = reverse('ordenes:ordenlocativos_change', args=[obj.pk])
        return format_html('<a class="button" href="{}">Editar</a>', url)
    editar_link.short_description = 'Editar'

    # Link “Eliminar” usando la URL estándar de Django Admin;
    # Jazzmin abrirá su modal de confirmación
    def eliminar_link(self, obj):
        # Si tu app_label es “ordenes” y el modelo “OrdenLocativos”:
        url = reverse('admin:ordenes_ordenlocativos_delete', args=[obj.pk])
        return format_html('<a class="button delete-btn" href="{}">Eliminar</a>', url)
    eliminar_link.short_description = 'Eliminar'

@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'tipo', 'estado', 'fecha_creacion']
    list_filter = ['tipo', 'estado', 'fecha_creacion']
    search_fields = ['cliente__nombre']
    filter_horizontal = ['trabajadores']

@admin.register(InspeccionGeneral)
class InspeccionGeneralAdmin(admin.ModelAdmin):
    list_display = ['orden']

@admin.register(DesinfeccionAmbientes)
class DesinfeccionAmbientesAdmin(admin.ModelAdmin):
    list_display = ['orden']

@admin.register(Zona)
class ZonaAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    filter_horizontal = ['tipos_empresa']

@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'zona']
    list_filter = ['zona']

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'unidad_medida']

@admin.register(CategoriaPlagas)
class CategoriaPlagasAdmin(admin.ModelAdmin):
    list_display = ['nombre']

@admin.register(Plaga)
class PlagaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria']

from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse
from .models import (
    TipoEmpresa,
    Orden,
    InspeccionGeneral,
    DesinfeccionAmbientes,
    Zona,
    Area,
    Material,
    OrdenLocativos,
)

@admin.register(OrdenLocativos)
class OrdenLocativosAdmin(admin.ModelAdmin):
    """
    Redirige las vistas de creación/edición al formulario personalizado en views.py
    """
    def add_view(self, request, form_url='', extra_context=None):
        return redirect(reverse('ordenes:ordenlocativos_add'))

    def change_view(self, request, object_id, form_url='', extra_context=None):
        return redirect(reverse('ordenes:ordenlocativos_change', args=[object_id]))

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

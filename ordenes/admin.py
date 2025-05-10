# ordenes/admin.py
from django.contrib import admin
from .models import (
    TipoEmpresa, Orden, InspeccionGeneral, OrdenLocativos, DesinfeccionAmbientes
)

@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre']

class OrdenAdmin(admin.ModelAdmin):
    list_display = ['id', 'cliente', 'get_tipo_empresa', 'tipo', 'estado', 'fecha_creacion']
    list_filter = ['tipo', 'estado', 'fecha_creacion']
    search_fields = ['cliente__nombre']
    filter_horizontal = ['trabajadores']
    readonly_fields = ['get_tipo_empresa']

    def get_tipo_empresa(self, obj):
        return obj.cliente.id_tipo.nombre if obj.cliente.id_tipo else "No definido"
    get_tipo_empresa.short_description = 'Tipo de Empresa'

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        if not change and obj.tipo == 'BENEFICIO':
            # Solo se crean si no existían antes (nueva orden)
            InspeccionGeneral.objects.create(orden=obj)
            OrdenLocativos.objects.create(orden=obj)
            DesinfeccionAmbientes.objects.create(orden=obj)

admin.site.register(Orden, OrdenAdmin)

@admin.register(InspeccionGeneral)
class InspeccionGeneralAdmin(admin.ModelAdmin):
    list_display = ['orden']

@admin.register(OrdenLocativos)
class OrdenLocativosAdmin(admin.ModelAdmin):
    list_display = ['orden']

@admin.register(DesinfeccionAmbientes)
class DesinfeccionAmbientesAdmin(admin.ModelAdmin):
    list_display = ['orden']

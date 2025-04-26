from django.contrib import admin
from .models import Usuario, Empleado, TipoInsecto, Insecto, Orden

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'correo', 'aprobado')
    search_fields = ('nombre', 'correo')
    list_filter = ('aprobado',)

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(TipoInsecto)
class TipoInsectoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'abreviado')
    search_fields = ('descripcion',)

@admin.register(Insecto)
class InsectoAdmin(admin.ModelAdmin):
    list_display = ('descripcion', 'tipo_insecto')
    search_fields = ('descripcion',)
    list_filter = ('tipo_insecto',)

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
    list_display = ('id', 'empleado', 'usuario', 'fecha_inicio', 'tipo_servicio', 'estado_envio')
    search_fields = ('usuario__nombre', 'empleado__nombre', 'tipo_servicio')
    list_filter = ('fecha_inicio', 'tipo_servicio', 'estado_envio')
    date_hierarchy = 'fecha_inicio'

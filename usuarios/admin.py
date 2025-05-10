# usuarios/admin.py
from django.contrib import admin
from .models import Cliente, Empleado

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'NIT', 'telefono', 'email', 'sede']
    search_fields = ['nombre', 'NIT', 'email']

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'cargo', 'user']
    search_fields = ['nombre', 'cargo']

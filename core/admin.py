from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cliente, FormatoFumigacion, Agenda

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'groups')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información Personal', {'fields': ('first_name', 'last_name', 'email', 'telefono', 'direccion')}),
        ('Permisos', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'role', 'email', 'first_name', 'last_name'),
        }),
    )
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'telefono', 'email', 'fecha_registro')
    search_fields = ('nombre', 'telefono', 'email')
    ordering = ('-fecha_registro',)

class FormatoFumigacionAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'trabajador', 'fecha_servicio', 'tipo_servicio', 'estado')
    list_filter = ('estado', 'fecha_servicio')
    search_fields = ('cliente__nombre', 'trabajador__username', 'tipo_servicio')
    ordering = ('-fecha_servicio',)

class AgendaAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'formato', 'fecha', 'estado')
    list_filter = ('estado', 'fecha')
    search_fields = ('trabajador__username', 'formato__cliente__nombre')
    ordering = ('fecha',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FormatoFumigacion, FormatoFumigacionAdmin)
admin.site.register(Agenda, AgendaAdmin)

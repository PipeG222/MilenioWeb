from django import forms
from django.forms import DateInput
from .models import SolicitudCita, Cliente, FormatoFumigacion

class SolicitudCitaForm(forms.ModelForm):
    class Meta:
        model = SolicitudCita
        fields = ['nombre', 'telefono', 'email', 'direccion', 'tipo_servicio', 'mensaje', 'fecha_preferencia']
        widgets = {
            'fecha_preferencia': DateInput(attrs={'type': 'date'}),
            'mensaje': forms.Textarea(attrs={'rows': 4}),
            'direccion': forms.Textarea(attrs={'rows': 2}),
        }

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'direccion']
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

class FormatoFumigacionForm(forms.ModelForm):
    class Meta:
        model = FormatoFumigacion
        fields = ['cliente', 'fecha_servicio', 'tipo_servicio', 'observaciones']
        widgets = {
            'fecha_servicio': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'rows': 4}),
        } 
from django import forms
from django.forms.models import ModelChoiceIteratorValue
from .models import OrdenLocativos, Zona, Area, Material, Orden

class OrdenWidget(forms.Select):
    """
    Widget personalizado para <select> de orden, añadiendo data-tipo-id.
    """
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super().create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        # Determinar PK real
        orden_pk = None
        if isinstance(value, ModelChoiceIteratorValue):
            orden_pk = value.value
        elif hasattr(value, 'pk'):
            orden_pk = value.pk
        # Añadir atributo data-tipo-id
        if orden_pk is not None:
            try:
                orden = Orden.objects.select_related('cliente__id_tipo').get(pk=orden_pk)
                tipo = orden.cliente.id_tipo
                if tipo:
                    option['attrs']['data-tipo-id'] = str(tipo.id)
            except Orden.DoesNotExist:
                pass
        return option

class OrdenLocativosForm(forms.ModelForm):
    orden = forms.ModelChoiceField(
        queryset=Orden.objects.select_related('cliente__id_tipo').all(),
        widget=OrdenWidget(attrs={'class': 'form-select'}),
        label='Orden'
    )
    zonas = forms.ModelMultipleChoiceField(
        queryset=Zona.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Zonas'
    )
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Áreas'
    )
    materiales = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Materiales'
    )
    cantidad_material = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Formato: material_id:cantidad, ej. "1:5,2:3"'
    )

    class Meta:
        model = OrdenLocativos
        fields = [
            'orden', 'tipo_servicio', 'observaciones', 'recomendaciones',
            'firma_operario', 'firma_acompanante', 'certificado'
        ]
        widgets = {
            'tipo_servicio': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
            'recomendaciones': forms.Textarea(attrs={'class': 'form-control', 'rows':3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Obtener tipo de empresa de la orden
        tipo_id = None
        if self.instance and self.instance.pk:
            tipo = self.instance.orden.cliente.id_tipo
            tipo_id = tipo.id if tipo else None
        elif 'orden' in self.data:
            try:
                orden_pk = int(self.data.get('orden'))
                orden = Orden.objects.select_related('cliente__id_tipo').get(pk=orden_pk)
                tipo = orden.cliente.id_tipo
                tipo_id = tipo.id if tipo else None
            except (ValueError, Orden.DoesNotExist):
                tipo_id = None
        # Filtrar zonas y áreas según tipo_id
        if tipo_id:
            self.fields['zonas'].queryset = Zona.objects.filter(tipos_empresa_id=tipo_id)
            self.fields['areas'].queryset = Area.objects.filter(zona__tipos_empresa=tipo_id)
        else:
            self.fields['zonas'].queryset = Zona.objects.none()
            self.fields['areas'].queryset = Area.objects.none()
        # Aplicar clases a restantes
        self.fields['orden'].widget.attrs.update({'id': 'id_orden'})
        self.fields['materiales'].widget.attrs.update({'id': 'id_materiales'})

from django import forms
from django.forms.models import ModelChoiceIteratorValue
from django.utils.translation import gettext_lazy as _
from .models import AreaLocativa, Higiene, OrdenLocativos, OrdenServicio, Producto, TipoServicio, Zona, Area, Material, Orden, Plaga

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
        widget=OrdenWidget(attrs={'class': 'form-select', 'id': 'id_orden'}),
        label='Orden'
    )
    especies = forms.ModelMultipleChoiceField(
        queryset=Plaga.objects.filter(activa=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_especies'}),
        label="Especies observadas"
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
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_materiales'}),
        label="Materiales"
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
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recomendaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Obtener tipo de empresa de la orden (si existe instancia o dato en POST)
        tipo_id = None
        if self.instance and self.instance.pk:
            tipo = self.instance.orden.cliente.id_tipo
            tipo_id = tipo.id if (tipo and hasattr(tipo, 'id')) else None
        elif 'orden' in self.data:
            try:
                orden_pk = int(self.data.get('orden'))
                orden = Orden.objects.select_related('cliente__id_tipo').get(pk=orden_pk)
                tipo = orden.cliente.id_tipo
                tipo_id = tipo.id if (tipo and hasattr(tipo, 'id')) else None
            except (ValueError, Orden.DoesNotExist):
                tipo_id = None

        # Filtrar queryset de zonas según el ManyToManyField 'tipos_empresa'
        if tipo_id:
            # Zona.tipos_empresa es ManyToMany, por lo que usamos __id
            self.fields['zonas'].queryset = Zona.objects.filter(tipos_empresa__id=tipo_id)
            # Para áreas, filtramos aquellas cuyo campo 'zona' está relacionado a una Zona
            # que tenga el tipo de empresa indicado:
            self.fields['areas'].queryset = Area.objects.filter(zona__tipos_empresa__id=tipo_id)
        else:
            self.fields['zonas'].queryset = Zona.objects.none()
            self.fields['areas'].queryset = Area.objects.none()

        # Asegurarse de que el campo 'orden' tenga el id correcto
        self.fields['orden'].widget.attrs.update({'id': 'id_orden'})
        # El widget de 'materiales' ya recibió en su declaración attrs={'id': 'id_materiales'}
    

class OrdenServicioForm(forms.ModelForm):
    orden = forms.ModelChoiceField(
        queryset=Orden.objects.select_related('cliente__id_tipo').all(),
        widget=OrdenWidget(attrs={'class': 'form-select', 'id': 'id_orden'}),
        label=_("Orden Principal")
    )
    tipo = forms.ModelChoiceField(
        queryset=TipoServicio.objects.all(),
        label=_("Tipo de Servicio"),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    
    higiene = forms.ModelChoiceField(
        queryset=Higiene.objects.all(),
        required=False,
        label=_("Higiene"),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_higiene'})
    )

    # Grupo de Áreas Locativas
    areaslocativas = forms.ModelMultipleChoiceField(
        queryset=AreaLocativa.objects.all(),
        required=False,
        label=_("Áreas Locativas"),
        widget=forms.SelectMultiple(attrs={
            'class': 'form-select',
            'id': 'id_areaslocativas',
            'size': '6'  # ajusta altura si quieres ver varias a la vez
        })
    )
    zonas = forms.ModelMultipleChoiceField(
        queryset=Zona.objects.none(),
        required=False,
        label=_("Zonas"),
        widget=forms.SelectMultiple(attrs={'class': 'form-select'})
    )
    areas = forms.ModelMultipleChoiceField(
        queryset=Area.objects.none(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        label='Áreas'
    )
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        required=False,
        label=_("Productos"),
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_productos'})
    )
    materiales = forms.ModelMultipleChoiceField(
        queryset=Material.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple(attrs={'id': 'id_materiales'}),
        label="Materiales"
    )
    cantidad_material = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text='Formato: material_id:cantidad, ej. "1:5,2:3"'
    )
    observaciones = forms.CharField(
        required=False,
        label=_("Observaciones"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    recomendaciones = forms.CharField(
        required=False,
        label=_("Recomendaciones"),
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )
    firma_operario = forms.ImageField(
        required=False,
        label=_("Firma Operario")
    )
    firma_acompanante = forms.ImageField(
        required=False,
        label=_("Firma Acompañante")
    )
    certificado = forms.FileField(
        required=False,
        label=_("Certificado")
    )

    class Meta:
        model = OrdenServicio
        fields = [
            'orden_principal',
            'tipo',
            'higiene',
            'areaslocativas',
            'zonas',
            'productos',
            'observaciones',
            'recomendaciones',
            'firma_operario',
            'firma_acompanante',
            'certificado',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Determinar tipo de cliente para filtrar zonas/áreas
        tipo_id = None

        # 1) Si ya existe instancia, tomamos su orden_principal
        if self.instance and self.instance.pk:
            orden = self.instance.orden_principal
            if hasattr(orden, 'cliente') and hasattr(orden.cliente, 'id_tipo'):
                tipo_id = orden.cliente.id_tipo.id

        # 2) Si viene en POST, lo obtenemos del campo
        elif 'orden_principal' in self.data:
            try:
                orden_pk = int(self.data.get('orden_principal'))
                orden = Orden.objects.select_related('cliente__id_tipo').get(pk=orden_pk)
                tipo_id = orden.cliente.id_tipo.id
            except (ValueError, Orden.DoesNotExist):
                tipo_id = None

        # Filtrar zonas y áreas según el tipo de empresa
        if tipo_id:
            # Zona.tipos_empresa es ManyToMany, por lo que usamos __id
            self.fields['zonas'].queryset = Zona.objects.filter(tipos_empresa__id=tipo_id)
            # Para áreas, filtramos aquellas cuyo campo 'zona' está relacionado a una Zona
            # que tenga el tipo de empresa indicado:
            self.fields['areas'].queryset = Area.objects.filter(zona__tipos_empresa__id=tipo_id)
        else:
            self.fields['zonas'].queryset = Zona.objects.none()
            self.fields['areas'].queryset = Area.objects.none()

        # Asegurarse de que el campo 'orden' tenga el id correcto
        self.fields['orden'].widget.attrs.update({'id': 'id_orden'})

        # Asegurarnos que el ID del widget coincida con el JS
        self.fields['orden_principal'].widget.attrs.update({'id': 'id_orden'})
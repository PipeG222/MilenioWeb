from django import forms
from common.models import Usuario, Empleado, Orden
import hashlib

class UsuarioForm(forms.ModelForm):
    """Formulario para crear y editar usuarios con gestión de contraseña"""
    password = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        help_text='Dejar en blanco para mantener la contraseña actual'
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(),
        required=False,
        label='Confirmar contraseña'
    )
    
    class Meta:
        model = Usuario
        fields = ['nombre', 'correo', 'password', 'password_confirm', 'idDevice', 'aprobado']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:  # si estamos editando
            self.fields['password'].help_text = 'Dejar en blanco para mantener la contraseña actual'
            self.fields['password_confirm'].help_text = 'Confirmar nueva contraseña si la cambias'
        else:  # si estamos creando
            self.fields['password'].required = True
            self.fields['password_confirm'].required = True
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password != password_confirm:
            self.add_error('password_confirm', 'Las contraseñas no coinciden')
            
        return cleaned_data
    
    def save(self, commit=True):
        usuario = super().save(commit=False)
        password = self.cleaned_data.get('password')
        
        if password:
            # Usar un método de hash más seguro
            password_hash = hashlib.sha256(password.encode()).hexdigest()
            usuario.password = password_hash
            
        if commit:
            usuario.save()
            
        return usuario

class EmpleadoForm(forms.ModelForm):
    """Formulario para crear y editar empleados"""
    class Meta:
        model = Empleado
        fields = ['nombre', 'foto']
        widgets = {
            'foto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'URL o datos base64 de la imagen'}),
        }

class OrdenFilterForm(forms.Form):
    """Formulario para filtrar órdenes"""
    q = forms.CharField(
        label='Buscar',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Buscar por nombre, tipo...', 'class': 'form-control'})
    )
    
    estado = forms.ChoiceField(
        label='Estado',
        required=False,
        choices=[('', 'Todos los estados')] + list(Orden.ESTADO_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    tipo = forms.ChoiceField(
        label='Tipo',
        required=False,
        choices=[('', 'Todos los tipos')] + list(Orden.TIPO_ORDEN_CHOICES),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    fecha_desde = forms.DateField(
        label='Fecha desde',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    fecha_hasta = forms.DateField(
        label='Fecha hasta',
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    ) 
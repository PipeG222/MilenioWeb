from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser, Cliente, FormatoFumigacion, Agenda, SolicitudCita
from django.contrib.auth.views import LoginView, LogoutView
from .forms import SolicitudCitaForm, ClienteForm, FormatoFumigacionForm
from django.db.models import Count, Q
from django.utils import timezone
from datetime import timedelta

def home(request):
    form = SolicitudCitaForm()
    
    if request.method == 'POST':
        form = SolicitudCitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Su solicitud de cita ha sido enviada exitosamente. Nos pondremos en contacto con usted pronto.')
            return redirect('home')
    
    return render(request, 'core/home.html', {'form': form})

def about(request):
    return render(request, 'core/about.html')

def services(request):
    return render(request, 'core/services.html')

def contact(request):
    form = SolicitudCitaForm()
    
    if request.method == 'POST':
        form = SolicitudCitaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Su mensaje ha sido enviado exitosamente. Nos pondremos en contacto con usted pronto.')
            return redirect('contact')
    
    return render(request, 'core/contact.html', {'form': form})

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        # Datos básicos
        formatos = FormatoFumigacion.objects.all().order_by('-fecha_creacion')
        trabajadores = CustomUser.objects.filter(role='trabajador')
        solicitudes = SolicitudCita.objects.filter(estado='pendiente').order_by('-fecha_solicitud')
        
        # Estadísticas para gráficos
        # Solicitudes por mes (últimos 6 meses)
        today = timezone.now()
        six_months_ago = today - timedelta(days=180)
        
        # Contar solicitudes por tipo de servicio para gráfico de pastel
        servicios_count = SolicitudCita.objects.values('tipo_servicio').annotate(
            count=Count('id')
        ).order_by('tipo_servicio')
        
        # Contar clientes únicos
        clientes_unicos = Cliente.objects.count()
        
        # Formatos por estado
        formatos_por_estado = FormatoFumigacion.objects.values('estado').annotate(
            count=Count('id')
        ).order_by('estado')
        
        context = {
            'formatos': formatos,
            'trabajadores': trabajadores,
            'solicitudes': solicitudes,
            'servicios_count': servicios_count,
            'clientes_unicos': clientes_unicos,
            'formatos_por_estado': formatos_por_estado,
        }
        return render(request, 'core/dashboard_admin.html', context)
    else:
        formatos = FormatoFumigacion.objects.filter(trabajador=request.user).order_by('-fecha_creacion')
        agendas = Agenda.objects.filter(trabajador=request.user).order_by('fecha')
        
        # Estadísticas básicas para trabajadores
        formatos_completados = formatos.filter(estado='aprobado').count()
        
        context = {
            'formatos': formatos,
            'agendas': agendas,
            'formatos_completados': formatos_completados
        }
        return render(request, 'core/dashboard_trabajador.html', context)

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'core/cliente_list.html'
    context_object_name = 'clientes'
    ordering = ['-fecha_registro']

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'core/cliente_form.html'
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

class FormatoFumigacionCreateView(LoginRequiredMixin, CreateView):
    model = FormatoFumigacion
    form_class = FormatoFumigacionForm
    template_name = 'core/formato_form.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.trabajador = self.request.user
        messages.success(self.request, 'Formato de fumigación creado exitosamente.')
        return super().form_valid(form)

class FormatoFumigacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FormatoFumigacion
    form_class = FormatoFumigacionForm
    template_name = 'core/formato_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form(self):
        form = super().get_form()
        if self.request.user.role != 'admin':
            form.fields.pop('estado', None)
        return form

    def test_func(self):
        formato = self.get_object()
        return self.request.user.role == 'admin' or formato.trabajador == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'Formato de fumigación actualizado exitosamente.')
        return super().form_valid(form)

@login_required
def agenda_create(request):
    if request.method == 'POST':
        formato_id = request.POST.get('formato')
        fecha = request.POST.get('fecha')
        trabajador_id = request.POST.get('trabajador')
        
        formato = get_object_or_404(FormatoFumigacion, id=formato_id)
        trabajador = get_object_or_404(CustomUser, id=trabajador_id)
        
        Agenda.objects.create(
            formato=formato,
            trabajador=trabajador,
            fecha=fecha
        )
        
        messages.success(request, 'Agenda creada exitosamente.')
        return redirect('dashboard')
        
    formatos = FormatoFumigacion.objects.filter(estado='pendiente')
    trabajadores = CustomUser.objects.filter(role='trabajador')
    return render(request, 'core/agenda_form.html', {
        'formatos': formatos,
        'trabajadores': trabajadores
    })

class SolicitudCitaListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = SolicitudCita
    template_name = 'core/solicitud_cita_list.html'
    context_object_name = 'solicitudes'
    ordering = ['-fecha_solicitud']
    
    def test_func(self):
        return self.request.user.role == 'admin'

class SolicitudCitaUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = SolicitudCita
    fields = ['estado']
    template_name = 'core/solicitud_cita_form.html'
    success_url = reverse_lazy('solicitud-list')
    
    def test_func(self):
        return self.request.user.role == 'admin'
    
    def form_valid(self, form):
        messages.success(self.request, 'Estado de la solicitud actualizado exitosamente.')
        return super().form_valid(form)

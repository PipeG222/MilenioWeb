from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import CustomUser, Cliente, FormatoFumigacion, Agenda
from django.contrib.auth.views import LoginView, LogoutView

def home(request):
    return render(request, 'core/home.html')

class CustomLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True

@login_required
def dashboard(request):
    if request.user.role == 'admin':
        formatos = FormatoFumigacion.objects.all().order_by('-fecha_creacion')
        trabajadores = CustomUser.objects.filter(role='trabajador')
        context = {
            'formatos': formatos,
            'trabajadores': trabajadores,
        }
        return render(request, 'core/dashboard_admin.html', context)
    else:
        formatos = FormatoFumigacion.objects.filter(trabajador=request.user).order_by('-fecha_creacion')
        agendas = Agenda.objects.filter(trabajador=request.user).order_by('fecha')
        context = {
            'formatos': formatos,
            'agendas': agendas,
        }
        return render(request, 'core/dashboard_trabajador.html', context)

class ClienteListView(LoginRequiredMixin, ListView):
    model = Cliente
    template_name = 'core/cliente_list.html'
    context_object_name = 'clientes'
    ordering = ['-fecha_registro']

class ClienteCreateView(LoginRequiredMixin, CreateView):
    model = Cliente
    template_name = 'core/cliente_form.html'
    fields = ['nombre', 'telefono', 'email', 'direccion']
    success_url = reverse_lazy('cliente-list')

    def form_valid(self, form):
        messages.success(self.request, 'Cliente creado exitosamente.')
        return super().form_valid(form)

class FormatoFumigacionCreateView(LoginRequiredMixin, CreateView):
    model = FormatoFumigacion
    template_name = 'core/formato_form.html'
    fields = ['cliente', 'fecha_servicio', 'tipo_servicio', 'observaciones']
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        form.instance.trabajador = self.request.user
        messages.success(self.request, 'Formato de fumigación creado exitosamente.')
        return super().form_valid(form)

class FormatoFumigacionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = FormatoFumigacion
    template_name = 'core/formato_form.html'
    fields = ['cliente', 'fecha_servicio', 'tipo_servicio', 'observaciones', 'estado']
    success_url = reverse_lazy('dashboard')

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

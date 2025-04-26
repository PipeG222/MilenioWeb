from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from common.models import Usuario, Empleado, TipoInsecto, Insecto, Orden

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = Usuario.objects.count()
        context['total_empleados'] = Empleado.objects.count()
        context['total_ordenes'] = Orden.objects.count()
        context['ordenes_recientes'] = Orden.objects.all().order_by('-fecha_inicio')[:5]
        return context

# Vistas para Usuario
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin_panel/usuario_list.html'
    context_object_name = 'usuarios'

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin_panel/usuario_detail.html'
    context_object_name = 'usuario'

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    template_name = 'admin_panel/usuario_form.html'
    fields = ['nombre', 'correo', 'password', 'idDevice', 'aprobado']
    success_url = reverse_lazy('admin_panel:usuario_list')

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    template_name = 'admin_panel/usuario_form.html'
    fields = ['nombre', 'correo', 'password', 'idDevice', 'aprobado']
    success_url = reverse_lazy('admin_panel:usuario_list')

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin_panel/usuario_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:usuario_list')

# Vistas para Empleado
class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'admin_panel/empleado_list.html'
    context_object_name = 'empleados'

class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    model = Empleado
    template_name = 'admin_panel/empleado_detail.html'
    context_object_name = 'empleado'

class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    template_name = 'admin_panel/empleado_form.html'
    fields = ['nombre', 'foto']
    success_url = reverse_lazy('admin_panel:empleado_list')

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    template_name = 'admin_panel/empleado_form.html'
    fields = ['nombre', 'foto']
    success_url = reverse_lazy('admin_panel:empleado_list')

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'admin_panel/empleado_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:empleado_list')

# Vistas para Orden
class OrdenListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'admin_panel/orden_list.html'
    context_object_name = 'ordenes'

class OrdenDetailView(LoginRequiredMixin, DetailView):
    model = Orden
    template_name = 'admin_panel/orden_detail.html'
    context_object_name = 'orden'

class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    template_name = 'admin_panel/orden_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_panel:orden_list')

class OrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Orden
    template_name = 'admin_panel/orden_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_panel:orden_list')

class OrdenDeleteView(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'admin_panel/orden_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:orden_list')

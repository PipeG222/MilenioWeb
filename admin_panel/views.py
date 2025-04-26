from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import Q, Count
from common.models import Usuario, Empleado, TipoInsecto, Insecto, Orden
from django.core.paginator import Paginator
from .forms import UsuarioForm, EmpleadoForm, OrdenFilterForm

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'admin_panel/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = Usuario.objects.count()
        context['total_empleados'] = Empleado.objects.count()
        context['total_ordenes'] = Orden.objects.count()
        context['ordenes_recientes'] = Orden.objects.all().order_by('-fecha_inicio')[:5]
        
        # Estadísticas adicionales
        context['ordenes_pendientes'] = Orden.objects.filter(estado_envio='pendiente').count()
        context['ordenes_completadas'] = Orden.objects.filter(estado_envio='completado').count()
        context['insectos_count'] = Insecto.objects.count()
        context['tipos_insectos_count'] = TipoInsecto.objects.count()
        
        return context

# Vistas para Usuario
class UsuarioListView(LoginRequiredMixin, ListView):
    model = Usuario
    template_name = 'admin_panel/usuario_list.html'
    context_object_name = 'usuarios'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Usuario.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) | 
                Q(correo__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class UsuarioDetailView(LoginRequiredMixin, DetailView):
    model = Usuario
    template_name = 'admin_panel/usuario_detail.html'
    context_object_name = 'usuario'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las últimas órdenes del usuario
        context['ordenes'] = self.object.orden_set.all().order_by('-fecha_inicio')
        return context

class UsuarioCreateView(LoginRequiredMixin, CreateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'admin_panel/usuario_form.html'
    success_url = reverse_lazy('admin_panel:usuario_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario creado correctamente')
        return super().form_valid(form)

class UsuarioUpdateView(LoginRequiredMixin, UpdateView):
    model = Usuario
    form_class = UsuarioForm
    template_name = 'admin_panel/usuario_form.html'
    success_url = reverse_lazy('admin_panel:usuario_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Usuario actualizado correctamente')
        return super().form_valid(form)

class UsuarioDeleteView(LoginRequiredMixin, DeleteView):
    model = Usuario
    template_name = 'admin_panel/usuario_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:usuario_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Usuario eliminado correctamente')
        return super().delete(request, *args, **kwargs)

# Vistas para Empleado
class EmpleadoListView(LoginRequiredMixin, ListView):
    model = Empleado
    template_name = 'admin_panel/empleado_list.html'
    context_object_name = 'empleados'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Empleado.objects.all()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query)
            )
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context

class EmpleadoDetailView(LoginRequiredMixin, DetailView):
    model = Empleado
    template_name = 'admin_panel/empleado_detail.html'
    context_object_name = 'empleado'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener las órdenes asignadas a este empleado
        context['ordenes'] = self.object.orden_set.all().order_by('-fecha_inicio')
        return context

class EmpleadoCreateView(LoginRequiredMixin, CreateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'admin_panel/empleado_form.html'
    success_url = reverse_lazy('admin_panel:empleado_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empleado creado correctamente')
        return super().form_valid(form)

class EmpleadoUpdateView(LoginRequiredMixin, UpdateView):
    model = Empleado
    form_class = EmpleadoForm
    template_name = 'admin_panel/empleado_form.html'
    success_url = reverse_lazy('admin_panel:empleado_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Empleado actualizado correctamente')
        return super().form_valid(form)

class EmpleadoDeleteView(LoginRequiredMixin, DeleteView):
    model = Empleado
    template_name = 'admin_panel/empleado_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:empleado_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Empleado eliminado correctamente')
        return super().delete(request, *args, **kwargs)

# Vistas para Orden
class OrdenListView(LoginRequiredMixin, ListView):
    model = Orden
    template_name = 'admin_panel/orden_list.html'
    context_object_name = 'ordenes'
    paginate_by = 10

    def get_queryset(self):
        queryset = Orden.objects.all().order_by('-fecha_inicio')
        
        # Usar el formulario de filtro
        filter_form = OrdenFilterForm(self.request.GET or None)
        
        if filter_form.is_valid():
            # Búsqueda por texto
            search_query = filter_form.cleaned_data.get('q')
            if search_query:
                queryset = queryset.filter(
                    Q(usuario__nombre__icontains=search_query) |
                    Q(empleado__nombre__icontains=search_query) |
                    Q(tipo_servicio__icontains=search_query) |
                    Q(detalles__icontains=search_query)
                )
            
            # Filtro por estado
            estado_filter = filter_form.cleaned_data.get('estado')
            if estado_filter:
                queryset = queryset.filter(estado_envio=estado_filter)
                
            # Filtro por tipo
            tipo_filter = filter_form.cleaned_data.get('tipo')
            if tipo_filter:
                queryset = queryset.filter(tipo_orden=tipo_filter)
                
            # Filtro por fecha
            fecha_desde = filter_form.cleaned_data.get('fecha_desde')
            if fecha_desde:
                queryset = queryset.filter(fecha_inicio__gte=fecha_desde)
                
            fecha_hasta = filter_form.cleaned_data.get('fecha_hasta')
            if fecha_hasta:
                queryset = queryset.filter(fecha_inicio__lte=fecha_hasta)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar el formulario de filtro al contexto
        context['filter_form'] = OrdenFilterForm(self.request.GET or None)
        
        # Mantener referencias a los filtros aplicados para la paginación
        context['search_query'] = self.request.GET.get('q', '')
        context['estado_filter'] = self.request.GET.get('estado', '')
        context['tipo_filter'] = self.request.GET.get('tipo', '')
        context['fecha_desde'] = self.request.GET.get('fecha_desde', '')
        context['fecha_hasta'] = self.request.GET.get('fecha_hasta', '')
        
        # Opciones para los filtros
        context['estado_opciones'] = Orden.ESTADO_CHOICES
        context['tipo_opciones'] = Orden.TIPO_ORDEN_CHOICES
        
        return context

class OrdenDetailView(LoginRequiredMixin, DetailView):
    model = Orden
    template_name = 'admin_panel/orden_detail.html'
    context_object_name = 'orden'

class OrdenCreateView(LoginRequiredMixin, CreateView):
    model = Orden
    template_name = 'admin_panel/orden_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_panel:orden_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.all()
        context['empleados'] = Empleado.objects.all()
        context['estado_opciones'] = Orden.ESTADO_CHOICES
        context['tipo_opciones'] = Orden.TIPO_ORDEN_CHOICES
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Orden creada correctamente')
        return super().form_valid(form)

class OrdenUpdateView(LoginRequiredMixin, UpdateView):
    model = Orden
    template_name = 'admin_panel/orden_form.html'
    fields = '__all__'
    success_url = reverse_lazy('admin_panel:orden_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['usuarios'] = Usuario.objects.all()
        context['empleados'] = Empleado.objects.all()
        context['estado_opciones'] = Orden.ESTADO_CHOICES
        context['tipo_opciones'] = Orden.TIPO_ORDEN_CHOICES
        return context
    
    def form_valid(self, form):
        messages.success(self.request, 'Orden actualizada correctamente')
        return super().form_valid(form)

class OrdenDeleteView(LoginRequiredMixin, DeleteView):
    model = Orden
    template_name = 'admin_panel/orden_confirm_delete.html'
    success_url = reverse_lazy('admin_panel:orden_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Orden eliminada correctamente')
        return super().delete(request, *args, **kwargs)

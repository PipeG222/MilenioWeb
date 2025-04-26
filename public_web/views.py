from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from common.models import Insecto, TipoInsecto, Orden

# Create your views here.

class HomeView(TemplateView):
    template_name = 'public_web/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_insectos'] = TipoInsecto.objects.all()[:6]
        return context

class ServiciosView(TemplateView):
    template_name = 'public_web/servicios.html'

class NosotrosView(TemplateView):
    template_name = 'public_web/nosotros.html'

class ContactoView(TemplateView):
    template_name = 'public_web/contacto.html'

class InsectosListView(ListView):
    model = Insecto
    template_name = 'public_web/insectos_list.html'
    context_object_name = 'insectos'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tipos_insectos'] = TipoInsecto.objects.all()
        return context

class InsectoDetailView(DetailView):
    model = Insecto
    template_name = 'public_web/insecto_detail.html'
    context_object_name = 'insecto'

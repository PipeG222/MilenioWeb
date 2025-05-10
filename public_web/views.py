from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView

# Create your views here.

class HomeView(TemplateView):
    template_name = 'public_web/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

class ServiciosView(TemplateView):
    template_name = 'public_web/servicios.html'

class NosotrosView(TemplateView):
    template_name = 'public_web/nosotros.html'

class ContactoView(TemplateView):
    template_name = 'public_web/contacto.html'
class InsectosListView(ListView):
    template_name = 'public_web/insectos_list.html'

class InsectoDetailView(DetailView):
    template_name = 'public_web/insecto_detail.html'

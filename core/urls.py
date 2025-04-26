from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('nosotros/', views.about, name='about'),
    path('servicios/', views.services, name='services'),
    path('contacto/', views.contact, name='contact'),
    
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    
    path('formatos/nuevo/', views.FormatoFumigacionCreateView.as_view(), name='formato-create'),
    path('formatos/<int:pk>/editar/', views.FormatoFumigacionUpdateView.as_view(), name='formato-update'),
    
    path('agenda/nueva/', views.agenda_create, name='agenda-create'),
    
    path('solicitudes/', views.SolicitudCitaListView.as_view(), name='solicitud-list'),
    path('solicitudes/<int:pk>/actualizar/', views.SolicitudCitaUpdateView.as_view(), name='solicitud-update'),
] 
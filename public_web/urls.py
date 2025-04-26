from django.urls import path
from . import views

app_name = 'public_web'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('servicios/', views.ServiciosView.as_view(), name='servicios'),
    path('nosotros/', views.NosotrosView.as_view(), name='nosotros'),
    path('contacto/', views.ContactoView.as_view(), name='contacto'),
    path('insectos/', views.InsectosListView.as_view(), name='insectos_list'),
    path('insectos/<int:pk>/', views.InsectoDetailView.as_view(), name='insecto_detail'),
] 
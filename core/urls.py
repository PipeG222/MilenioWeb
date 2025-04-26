from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('clientes/', views.ClienteListView.as_view(), name='cliente-list'),
    path('clientes/nuevo/', views.ClienteCreateView.as_view(), name='cliente-create'),
    path('formatos/nuevo/', views.FormatoFumigacionCreateView.as_view(), name='formato-create'),
    path('formatos/<int:pk>/editar/', views.FormatoFumigacionUpdateView.as_view(), name='formato-update'),
    path('agenda/nueva/', views.agenda_create, name='agenda-create'),
] 
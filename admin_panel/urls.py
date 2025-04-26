from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    
    # URLs para Usuario
    path('usuarios/', views.UsuarioListView.as_view(), name='usuario_list'),
    path('usuarios/<int:pk>/', views.UsuarioDetailView.as_view(), name='usuario_detail'),
    path('usuarios/nuevo/', views.UsuarioCreateView.as_view(), name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.UsuarioUpdateView.as_view(), name='usuario_update'),
    path('usuarios/<int:pk>/eliminar/', views.UsuarioDeleteView.as_view(), name='usuario_delete'),
    
    # URLs para Empleado
    path('empleados/', views.EmpleadoListView.as_view(), name='empleado_list'),
    path('empleados/<int:pk>/', views.EmpleadoDetailView.as_view(), name='empleado_detail'),
    path('empleados/nuevo/', views.EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleados/<int:pk>/editar/', views.EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleados/<int:pk>/eliminar/', views.EmpleadoDeleteView.as_view(), name='empleado_delete'),
    
    # URLs para Orden
    path('ordenes/', views.OrdenListView.as_view(), name='orden_list'),
    path('ordenes/<int:pk>/', views.OrdenDetailView.as_view(), name='orden_detail'),
    path('ordenes/nueva/', views.OrdenCreateView.as_view(), name='orden_create'),
    path('ordenes/<int:pk>/editar/', views.OrdenUpdateView.as_view(), name='orden_update'),
    path('ordenes/<int:pk>/eliminar/', views.OrdenDeleteView.as_view(), name='orden_delete'),
] 
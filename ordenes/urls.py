from django.urls import path
from . import views

app_name = 'ordenes'

urlpatterns = [
    path('ordenlocativos/add/', views.ordenlocativos_add, name='ordenlocativos_add'),
    path('ordenlocativos/<int:pk>/change/', views.ordenlocativos_change, name='ordenlocativos_change'),
    path('api/zones/<int:tipo_id>/', views.api_zones_by_tipo, name='api_zones_by_tipo'),
    path('api/areas/<int:zone_id>/', views.api_areas_by_zone, name='api_areas_by_zone'),
]

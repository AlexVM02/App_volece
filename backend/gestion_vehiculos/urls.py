from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VehiculoViewSet, VehiculoTransportistaView,VehiculoEstadoUpdateView, MantenimientoTransportistaView
from .views import AlertasMantenimientoView, ActualizarKilometrajeView

# Router para el ADMIN
router = DefaultRouter()
router.register(r'', VehiculoViewSet, basename='vehiculos')

urlpatterns = [
    # URLs para el admin 
    path('', include(router.urls)),

    # URL para el Transportista
    path('transportista/vehiculo', VehiculoTransportistaView.as_view(), name='vehiculo-transportista'),
    path('transportista/vehiculo/estado', VehiculoEstadoUpdateView.as_view(), name='vehiculo-estado-update'),
    path('transportista/mantenimientos', MantenimientoTransportistaView.as_view(), name='mantenimiento-transportista'),
    path('transportista/alertas', AlertasMantenimientoView.as_view(), name='alertas-mantenimiento'),
    path('transportista/vehiculo/kilometraje', ActualizarKilometrajeView.as_view(), name='actualizar-kilometraje'),
    ]



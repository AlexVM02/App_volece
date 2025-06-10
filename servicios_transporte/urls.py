from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CrearSolicitudServicioView
from .views import ListaSolicitudesClienteView
from .views import ListaSolicitudesAdminView
from .views import SolicitudDetailView


urlpatterns = [
    path('solicitudes/crear/', CrearSolicitudServicioView.as_view(), name='crear-solicitud'),
    path('solicitudes/mis-solicitudes/', ListaSolicitudesClienteView.as_view(), name='mis-solicitudes'),
    path('solicitudes/', ListaSolicitudesAdminView.as_view(), name='solicitudes-admin'),
    path('solicitudes/<int:pk>/', SolicitudDetailView.as_view(), name='solicitud-detail'),
    path('solicitudes/todas/', ListaSolicitudesAdminView.as_view(), name='solicitudes-admin'),
]

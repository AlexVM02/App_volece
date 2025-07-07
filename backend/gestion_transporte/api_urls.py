# gestion_transporte/api_urls.py
from django.urls import path
from .views import AsignarTurnoIAView

urlpatterns = [
    path('asignar-turno/', AsignarTurnoIAView.as_view(), name='asignar_turno_ia'),
]

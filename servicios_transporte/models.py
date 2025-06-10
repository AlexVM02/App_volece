from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class SolicitudServicio(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('asignado', 'Asignado'),
        ('completado', 'Completado'),
        ('rechazado', 'Rechazado'),
    ]

    cliente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitudes')
    origen = models.CharField(max_length=256)
    destino = models.CharField(max_length=255)
    tipo_carga = models.CharField(max_length=100)
    fecha_solicitud = models.DateField()
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

def __str__(self):
    return f"{self.origen} → {self.destino} ({self.estado})"

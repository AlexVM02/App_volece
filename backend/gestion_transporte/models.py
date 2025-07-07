from django.db import models
from gestion_usuarios.models import Usuario

class DatasetTurnosIA(models.Model):
    transportista = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        limit_choices_to={'rol': 'TRANSP'}
    )
    fecha_turno = models.DateField()
    disponible = models.BooleanField()
    estado_vehiculo = models.CharField(max_length=20, choices=[
        ('activo', 'Activo'),
        ('inactivo', 'Inactivo'),
        ('mantenimiento', 'Mantenimiento')
    ])
    vehiculo_operativo = models.BooleanField()
    turno_asignado = models.BooleanField()

    def __str__(self):
        return f"Turno para {self.transportista} el {self.fecha_turno}"

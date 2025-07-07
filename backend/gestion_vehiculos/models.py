from django.db import models
from django.conf import settings

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('VOLQUETA', 'Volqueta'),
        ('CAMION', 'Camión'),
        ('TRAILER', 'Trailer'),
        ('FURGON', 'Furgón'),
        ('OTRO', 'Otro'),
    ]

    COMBUSTIBLE_CHOICES = [
        ('DIESEL', 'Diesel'),
        ('GASOLINA', 'Gasolina'),
        ('ELECTRICO', 'Eléctrico'),
        ('HIBRIDO', 'Híbrido'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
    ]

    transportista = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        limit_choices_to={'groups__name': 'Transportista'}
    )
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    placa = models.CharField(max_length=10, unique=True)
    anio = models.IntegerField()
    color = models.CharField(max_length=50)
    tonelaje = models.DecimalField(max_digits=5, decimal_places=2)
    combustible = models.CharField(max_length=15, choices=COMBUSTIBLE_CHOICES)
    numero_motor = models.CharField(max_length=50, blank=True, null=True)
    numero_chasis = models.CharField(max_length=50, blank=True, null=True)
    fecha_adquisicion = models.DateField(null=True, blank=True)
    observaciones = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')
    kilometraje_actual = models.PositiveIntegerField(default=0)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.placa} - {self.marca} {self.modelo}"

#modelo para el mantenimiento de los vehiculos

class Mantenimiento(models.Model):
    TIPO_MANTENIMIENTO_CHOICES = [
        ('CAMBIO_ACEITE', 'Cambio de Aceite'),
        ('FILTROS', 'Cambio de Filtros'),
        ('FRENOS', 'Revisión de Frenos'),
        ('LLANTAS', 'Revisión de Llantas'),
        ('SUSPENSION', 'Revisión de Suspensión'),
        ('ELECTRICO', 'Sistema Eléctrico'),
        ('REFRIGERACION', 'Sistema de Refrigeración'),
        ('OTRO', 'Otro')
    ]

    vehiculo = models.ForeignKey('Vehiculo', on_delete=models.CASCADE, related_name='mantenimientos')
    tipo = models.CharField(
        max_length=50, 
        choices=TIPO_MANTENIMIENTO_CHOICES, 
        default='CAMBIO_ACEITE'
    )
    kilometraje_actual = models.PositiveIntegerField()
    kilometraje_proximo = models.PositiveIntegerField(default=0)
    fecha_mantenimiento = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)
  

    def __str__(self):
        return f"{self.vehiculo.placa} - {self.tipo} ({self.fecha_mantenimiento})"

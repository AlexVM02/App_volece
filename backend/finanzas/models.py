from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone  # Asegúrate de que timezone está importado
from datetime import date

# Asegúrate de que estamos usando el modelo correcto de usuario
User = settings.AUTH_USER_MODEL

class CuotaMensual(models.Model):
    # Relación con el modelo User (socios)
    socio = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cuotas')
    
    # El mes y año de la cuota
    mes = models.DateField()  
    
    # Monto de la cuota, por defecto es $25
    monto = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=settings.CUOTA_MENSUAL_DEFAULT
    )
    
    # Estado de la cuota: 'pendiente' o 'pagado'
    estado = models.CharField(
        max_length=20, 
        choices=[('pendiente', 'Pendiente'), ('pagado', 'Pagado')], 
        default='pendiente'
    )  
    
    # Fecha de pago, si está pagada
    fecha_pago = models.DateField(null=True, blank=True)  
    
    # Fecha de creación de la cuota
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cuota de {self.socio} - {self.monto} - {self.mes} - Estado: {self.estado}"

    def clean(self):
        """
        Validación de duplicados: verifica si ya existe una cuota para el mismo mes y socio.
        Esto asegura que no se repita una cuota para el mismo mes.
        """
        # Verificar si ya existe una cuota registrada para el mismo socio y mes
        if CuotaMensual.objects.filter(
            socio=self.socio,
            mes__year=self.mes.year,
            mes__month=self.mes.month
        ).exclude(pk=self.pk).exists():
            raise ValidationError("Ya existe una cuota registrada para este mes.")
    
    def save(self, *args, **kwargs):
        """
        Sobrescribir el método save para llamar a clean() antes de guardar la cuota.
        """
        self.clean()  # Validar antes de guardar
        super(CuotaMensual, self).save(*args, **kwargs)

    def marcar_como_pagada(self):
        """
        Método para marcar la cuota como pagada y registrar la fecha de pago.
        """
        if self.estado == 'pendiente':
            self.estado = 'pagado'
            self.fecha_pago = timezone.now()  # Asignar la fecha actual como fecha de pago
            self.monto = settings.CUOTA_MENSUAL_DEFAULT
            self.save()

    @classmethod
    def crear_cuota(cls, socio, mes):
        """
        Método para crear cuotas mensuales automáticamente.
        """
        cuota = cls(socio=socio, mes=mes)
        cuota.save()  # Guardar la cuota, validando que no exista una cuota para ese mes
        return cuota

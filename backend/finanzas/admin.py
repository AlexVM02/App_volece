"""from django.contrib import admin
from .models import MovimientoFinanciero, FacturaServicio
from gestion_usuarios.models import Usuario  

class MovimientoFinancieroAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'tipo', 'monto', 'origen', 'socio', 'registrado_por')
    list_filter = ('tipo', 'origen')
    search_fields = ('descripcion',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'socio':
            kwargs["queryset"] = Usuario.objects.filter(rol='TRANSP')
        elif db_field.name == 'registrado_por':
            kwargs["queryset"] = Usuario.objects.filter(rol='ADMIN')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


class FacturaServicioAdmin(admin.ModelAdmin):
    list_display = (
        'cliente_externo',
        'monto_total',
        'estado_pago',
        'aplicar_retencion',
        'socio',
        'fecha_servicio'
    )
    list_filter = ('estado_pago', 'fecha_servicio', 'aplicar_retencion')
    search_fields = ('cliente_externo',)
    actions = ['registrar_pago_factura']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'socio':
            kwargs["queryset"] = Usuario.objects.filter(rol='TRANSP')
        elif db_field.name == 'registrado_por':
            kwargs["queryset"] = Usuario.objects.filter(rol='ADMIN')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def registrar_pago_factura(self, request, queryset):
        for factura in queryset:
            factura.registrar_pago()
        self.message_user(request, "Factura(s) procesada(s) correctamente.")
    registrar_pago_factura.short_description = "Registrar pago del cliente y generar movimientos"

admin.site.register(MovimientoFinanciero, MovimientoFinancieroAdmin)
admin.site.register(FacturaServicio, FacturaServicioAdmin)
"""
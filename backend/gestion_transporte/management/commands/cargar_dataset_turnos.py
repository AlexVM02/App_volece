from django.core.management.base import BaseCommand
from gestion_usuarios.models import Usuario
from gestion_transporte.models import DatasetTurnosIA
from django.utils import timezone
import random
from datetime import timedelta

class Command(BaseCommand):
    help = 'Genera 50 transportistas y 5000 registros en DatasetTurnosIA'

    def handle(self, *args, **kwargs):
        # Crea 50 transportistas porque no existen
        transportistas = Usuario.objects.filter(rol='TRANSP')
        faltantes = 50 - transportistas.count()
        created_ids = []

        if faltantes > 0:
            self.stdout.write(f"Creando {faltantes} transportistas...")
            for i in range(faltantes):
                t = Usuario.objects.create_user(
                    username=f'transportista{i}',
                    email=f'transportista{i}@correo.com',
                    password='12345678',
                    first_name=f'Trans{i}',
                    last_name='Demo',
                    cedula_ruc=f'100000{i:04d}',
                    telefono='0999999999',
                    rol='TRANSP'
                )
                created_ids.append(t.id)

        transportistas = Usuario.objects.filter(rol='TRANSP')
        ids = list(transportistas.values_list('id', flat=True))

        DatasetTurnosIA.objects.all().delete()
        self.stdout.write("Generando registros del dataset IA...")

        base_date = timezone.now().date()
        estados = ['activo', 'inactivo', 'mantenimiento']
        registros = []

        for _ in range(5000):
            tid = random.choice(ids)
            fecha = base_date - timedelta(days=random.randint(0, 180))
            disponible = random.choices([True, False], weights=[90, 10])[0]
            estado = random.choice(estados)
            operativo = estado == 'activo'
            turno_asignado = int(disponible and operativo)

            registros.append(DatasetTurnosIA(
                transportista_id=tid,
                fecha_turno=fecha,
                disponible=disponible,
                estado_vehiculo=estado,
                vehiculo_operativo=operativo,
                turno_asignado=turno_asignado
            ))

        DatasetTurnosIA.objects.bulk_create(registros)
        self.stdout.write(self.style.SUCCESS("Datos generados correctamente: 50 transportistas y 5000 registros."))


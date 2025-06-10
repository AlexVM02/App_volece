from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.utils import timezone
from .models import CuotaMensual
from datetime import date
from .serializers import CuotaMensualSerializer, UsuarioSerializer  # Importar los serializadores correctos

from rest_framework.decorators import api_view  # Importamos el decorador api_view

User = get_user_model()  # Usamos get_user_model() para obtener el modelo de usuario configurado

# Vista para listar usuarios (socios) con rol 'TRANSP'
class UsuarioListView(generics.ListAPIView):
    queryset = User.objects.all()  # Usamos get_user_model() para obtener el modelo de usuario
    serializer_class = UsuarioSerializer  # Usamos el serializador de usuarios
    permission_classes = [IsAuthenticated]  # Solo accesible por usuarios autenticados

    def get_queryset(self):
        rol = self.request.query_params.get('rol', None)
        if rol == 'TRANSP':
            return self.queryset.filter(rol='TRANSP')  # Filtramos por rol 'TRANSP'
        return self.queryset


# Vista para registrar una cuota mensual
class RegistrarCuotaView(generics.CreateAPIView):
    queryset = CuotaMensual.objects.all()
    serializer_class = CuotaMensualSerializer  # Usamos el serializador correcto
    permission_classes = [IsAuthenticated]  # Solo accesible por usuarios autenticados

    def post(self, request, *args, **kwargs):
        # Verificamos si ya existe una cuota para el mismo mes y socio
        socio = request.data.get('socio')
        mes = request.data.get('mes')

        # Si ya existe una cuota para el mismo mes y socio, lanzamos un error
        if CuotaMensual.objects.filter(socio=socio, mes=mes).exists():
            return Response({'error': 'Ya existe una cuota registrada para este mes.'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Si no existe, guardamos la nueva cuota
        return super().post(request, *args, **kwargs)


# Vista para listar las cuotas mensuales
class ListarCuotasView(generics.ListAPIView):
    queryset = CuotaMensual.objects.all()
    serializer_class = CuotaMensualSerializer  # Usamos el serializador correcto
    permission_classes = [IsAuthenticated]  # Solo accesible por usuarios autenticados


# Vista para obtener todas las cuotas (pendientes y pagadas)
@api_view(['GET'])
def obtener_todas_las_cuotas(request):
    """
    Obtener todas las cuotas (pendientes y pagadas).
    """
    cuotas = CuotaMensual.objects.all()  # Obtener todas las cuotas
    
    # Serializamos las cuotas
    cuotas_data = CuotaMensualSerializer(cuotas, many=True).data

    return Response(cuotas_data)


# Vista para obtener las cuotas pendientes de todos los socios
class ObtenerCuotasPendientesView(generics.ListAPIView):
    queryset = CuotaMensual.objects.filter(estado='pendiente')
    serializer_class = CuotaMensualSerializer
    permission_classes = [IsAuthenticated]  # Solo accesible por usuarios autenticados

    def get_queryset(self):
        # Filtrar solo a los socios con rol 'TRANSP' (transportistas)
        transportistas = User.objects.filter(rol='TRANSP')
        return CuotaMensual.objects.filter(socio__in=transportistas, estado='pendiente')


# Vista para actualizar el estado de la cuota a 'pagado' y registrar la fecha de pago
class MarcarCuotaPagadaView(generics.UpdateAPIView):
    queryset = CuotaMensual.objects.all()
    serializer_class = CuotaMensualSerializer  # Usamos el serializador correcto
    permission_classes = [IsAuthenticated]  # Solo accesible por usuarios autenticados

    def update(self, request, *args, **kwargs):
        cuota = get_object_or_404(CuotaMensual, id=kwargs['pk'])

        # Cambiar el estado a 'pagado' y registrar la fecha de pago
        if cuota.estado == 'pendiente':
            cuota.estado = 'pagado'
            cuota.fecha_pago = timezone.now()  # Asignar la fecha actual como fecha de pago
            cuota.monto = 25  # Asegurarse de que el monto sea 25$
            cuota.save()

            return Response({
                'message': 'Estado de la cuota actualizado con éxito',
                'estado': cuota.estado,
                'fecha_pago': cuota.fecha_pago,
                'monto': cuota.monto
            })
        else:
            return Response({'error': 'La cuota ya está marcada como pagada.'}, status=status.HTTP_400_BAD_REQUEST)


class CrearCuotasMensualesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Verifica si el usuario es admin
        if request.user.rol != 'ADMIN':
            return Response({'detail': 'No autorizado. Solo administradores pueden crear cuotas.'}, status=status.HTTP_403_FORBIDDEN)

        # Crear cuotas para los transportistas
        socios = User.objects.filter(rol='TRANSP')  # Filtrar por transportistas (rol 'TRANSP')
        mes_actual = date.today().replace(day=1)  # Primer día del mes

        for socio in socios:
            # Crear la cuota mensual para cada socio, evitando duplicados
            cuota, created = CuotaMensual.objects.get_or_create(
                socio=socio, 
                mes=mes_actual, 
                defaults={'monto': 25.00, 'estado': 'pendiente'}
            )
            if created:
                print(f"Cuota creada para {socio.username} del mes {mes_actual}.")
            else:
                print(f"Ya existe una cuota para {socio.username} en el mes {mes_actual}.")

        return Response({'detail': 'Cuotas creadas exitosamente.'}, status=status.HTTP_201_CREATED)
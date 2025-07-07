from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Vehiculo, Mantenimiento
from .serializer import VehiculoSerializer, VehiculoTransportistaSerializer, MantenimientoSerializer


# Vista para el Admin
class VehiculoViewSet(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.IsAdminUser]

# Vista para el Transportista
class VehiculoTransportistaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            serializer = VehiculoTransportistaSerializer(vehiculo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'No se encontró vehículo registrado'}, status=status.HTTP_404_NOT_FOUND)



class VehiculoEstadoUpdateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        nuevo_estado = request.data.get('estado')

        if nuevo_estado not in ['ACTIVO', 'INACTIVO', 'MANTENIMIENTO']:
            return Response({'error': 'Estado no válido'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            vehiculo.estado = nuevo_estado
            vehiculo.save()
            return Response({'mensaje': f'Estado actualizado a {nuevo_estado}'}, status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class MantenimientoTransportistaView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            mantenimientos = Mantenimiento.objects.filter(vehiculo=vehiculo).order_by('-fecha_mantenimiento')
            serializer = MantenimientoSerializer(mantenimientos, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'No tiene vehículo asignado'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            data = request.data.copy()
            data['vehiculo'] = vehiculo.id

            serializer = MantenimientoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'No tiene vehículo asignado'}, status=status.HTTP_404_NOT_FOUND)
        
#vista para alertas de mantenimiento   
class AlertasMantenimientoView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        margen_alerta = 500  # margen de anticipación (500 km)
        alertas = []

        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            mantenimientos = Mantenimiento.objects.filter(vehiculo=vehiculo).order_by('-fecha_mantenimiento')

            for mantenimiento in mantenimientos:
                km_restante = mantenimiento.kilometraje_proximo - vehiculo.kilometraje_actual

                if km_restante <= margen_alerta:
                    tipo_mostrar = mantenimiento.get_tipo_display()
                    mensaje = f"Próximo {tipo_mostrar} a los {mantenimiento.kilometraje_proximo} km. Quedan {km_restante} km."
                    alertas.append({'mensaje': mensaje})

            return Response(alertas, status=status.HTTP_200_OK)

        except Vehiculo.DoesNotExist:
            return Response({'error': 'No tiene vehículo asignado'}, status=status.HTTP_404_NOT_FOUND)


# vista para actualizar el kilometraje del vehículo
class ActualizarKilometrajeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request):
        nuevo_kilometraje = request.data.get('kilometraje_actual')

        if nuevo_kilometraje is None:
            return Response({'error': 'Debe enviar el nuevo kilometraje_actual'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            vehiculo = Vehiculo.objects.get(transportista=request.user)
            vehiculo.kilometraje_actual = nuevo_kilometraje
            vehiculo.save()
            return Response({'mensaje': 'Kilometraje actualizado correctamente'}, status=status.HTTP_200_OK)
        except Vehiculo.DoesNotExist:
            return Response({'error': 'Vehículo no encontrado'}, status=status.HTTP_404_NOT_FOUND)
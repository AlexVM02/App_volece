from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from servicios_transporte.models import SolicitudServicio
from gestion_usuarios.models import Usuario
from gestion_vehiculos.models import Vehiculo
import joblib
import os
import pandas as pd  # Importamos pandas para trabajar con DataFrames

# Ruta del modelo .pkl entrenado
MODELO_PATH = os.path.join(os.path.dirname(__file__), 'modelos', 'modelo_turnos.pkl')
modelo_ia = joblib.load(MODELO_PATH)

class AsignarTurnoIAView(APIView):
    permission_classes = [AllowAny]  # Ajuste para pruebas, cambiar a algo más seguro en producción

    def post(self, request):
        # Obtener la solicitud por ID
        id_solicitud = request.data.get('id_solicitud')
        if not id_solicitud:
            return Response({'error': 'Falta el ID de la solicitud'}, status=400)
        
        solicitud = get_object_or_404(SolicitudServicio, id=id_solicitud)
        
        # Filtrar transportistas cuyo vehículo esté en estado 'ACTIVO'
        transportistas = Usuario.objects.filter(rol='TRANSP')  # Asegúrate de tener el campo 'rol'
        transportistas_disponibles = transportistas.filter(
            vehiculo__estado='ACTIVO'  # Filtramos por el estado del vehículo en Vehiculo
        )

        # Almacenamos los resultados de predicción para cada transportista
        resultados = []
        
        for transportista in transportistas_disponibles:
            # Verificar que el transportista tenga un vehículo relacionado
            vehiculo = Vehiculo.objects.filter(transportista=transportista).first()

            if vehiculo:
                disponible = True  # Si está disponible
                vehiculo_operativo = True  # Si el vehículo está operativo 
                
                entrada = pd.DataFrame([{
                    'disponible': disponible,
                    'vehiculo_operativo': vehiculo_operativo,
                    'estado_vehiculo_activo': 1 if vehiculo.estado == 'ACTIVO' else 0,
                    'estado_vehiculo_inactivo': 1 if vehiculo.estado == 'INACTIVO' else 0,
                    'estado_vehiculo_mantenimiento': 1 if vehiculo.estado == 'MANTENIMIENTO' else 0
                }])

                # Hacer la predicción
                resultado = modelo_ia.predict(entrada)[0]
                probabilidad = modelo_ia.predict_proba(entrada)[0][1]

                # Depuración: Imprimir el nombre del transportista
                print(f"Transportista: {transportista.first_name} {transportista.last_name}")
                
                resultados.append({
                    'transportista_nombre': f"{transportista.first_name} {transportista.last_name}",
                    'probabilidad': round(probabilidad, 2),
                    'asignar_turno': bool(resultado),
                })

        # Verificar si hay resultados disponibles
        if not resultados:
            return Response({'error': 'No hay transportistas disponibles para asignar'}, status=404)

        # Seleccionar el mejor transportista basado en la probabilidad más alta
        mejor_transportista = max(resultados, key=lambda x: x['probabilidad'])

        return Response({
            'mejor_transportista': mejor_transportista
        })

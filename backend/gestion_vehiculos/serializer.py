from rest_framework import serializers
from .models import Vehiculo, Mantenimiento
from gestion_usuarios.models import Usuario



class TransportistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id', 'username', 'first_name', 'last_name']

class VehiculoSerializer(serializers.ModelSerializer):
    transportista = serializers.PrimaryKeyRelatedField(
        queryset=Usuario.objects.filter(rol='TRANSP'),
        write_only=True
    )

    transportista_detalle = TransportistaSerializer(source='transportista', read_only=True)

    class Meta:
        model = Vehiculo
        fields = '__all__'

class VehiculoTransportistaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = [
            'id', 'tipo', 'marca', 'modelo', 'placa', 'anio',
            'color', 'tonelaje', 'combustible', 'estado'
        ]

class MantenimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mantenimiento
        fields = ['id', 'vehiculo', 'tipo', 'kilometraje_actual', 'kilometraje_proximo', 'fecha_mantenimiento', 'observaciones']
        read_only_fields = ['fecha_mantenimiento']


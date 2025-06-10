from rest_framework import serializers
from django.contrib.auth import get_user_model

Usuario = get_user_model()

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'rol',
            'cedula_ruc',
            'password'
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        rol_recibido = validated_data.get('rol', 'CLIENTE')

        request = self.context.get('request')
        current_user_rol = getattr(request.user, 'rol', None) if request and request.user.is_authenticated else None

        # Determinar el rol final según quién crea
        rol_final = rol_recibido if current_user_rol == 'ADMIN' else 'CLIENTE'
        
        validated_data.pop('rol', None)

        user = Usuario(**validated_data)
        user.set_password(password)
        user.rol = rol_final
        user.save()
        return user
    
# Clase para la edición de usuarios del administrador
class UsuarioEdicionAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'rol', 'cedula_ruc']

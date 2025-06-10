from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CuotaMensual

User = get_user_model()  # Usamos el modelo de usuario configurado en settings

class UsuarioSerializer(serializers.ModelSerializer):
    # Agregamos el campo 'nombre_completo' para concatenar 'first_name' y 'last_name' del socio (transportista)
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = User  # Usamos el modelo de usuario configurado
        fields = ['id', 'username', 'email', 'rol', 'nombre_completo']  # Campos a incluir en la respuesta

    def get_nombre_completo(self, obj):
        # Concatenamos el 'first_name' y 'last_name' del socio para mostrar el nombre completo
        nombre = obj.first_name or ''  # Asegurarnos de que 'first_name' no sea None
        apellido = obj.last_name or ''  # Asegurarnos de que 'last_name' no sea None
        return f"{nombre} {apellido}".strip() or obj.username  # Si no hay nombre, usar 'username'



User = get_user_model()  # Usamos el modelo de usuario configurado en settings

class CuotaMensualSerializer(serializers.ModelSerializer):
    # Agregamos el campo 'nombre_completo' para concatenar 'first_name' y 'last_name' del socio (transportista)
    nombre_completo = serializers.SerializerMethodField()

    class Meta:
        model = CuotaMensual
        fields = ['id', 'socio', 'nombre_completo', 'mes', 'monto', 'fecha_pago', 'estado']  # Los campos que debe manejar el formulario

    def get_nombre_completo(self, obj):
        # Concatenamos el 'first_name' y 'last_name' del socio para mostrar el nombre completo
        nombre = obj.socio.first_name or ''  # Asegurarnos de que 'first_name' no sea None
        apellido = obj.socio.last_name or ''  # Asegurarnos de que 'last_name' no sea None
        return f"{nombre} {apellido}".strip() or obj.socio.username  # Si no hay nombre, usar 'username'

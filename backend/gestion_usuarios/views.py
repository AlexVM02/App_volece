from rest_framework import generics
from .models import Usuario
from .serializers import UsuarioSerializer
from gestion_usuarios.serializers import UsuarioEdicionAdminSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from gestion_usuarios.models import Usuario
from gestion_usuarios.serializers import UsuarioSerializer
# recuperación de contraseña
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
#lista de transportistas
from django.contrib.auth.models import User



class RegistroUsuarioView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [AllowAny]  

    def post(self, request):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


    
class CrearUsuarioPrivadoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.rol != 'ADMIN':
            return Response({'detail': 'No autorizado. Solo administradores pueden crear usuarios.'}, status=status.HTTP_403_FORBIDDEN)

        serializer = UsuarioSerializer(data=request.data, context={'request': request})
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'detail': 'Usuario creado exitosamente.'}, status=status.HTTP_201_CREATED)
    
    
class PerfilUsuarioView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data)

# Listar usuarios
class ListarUsuariosView(ListAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]
    

# Eliminar usuario
class EliminarUsuarioView(generics.DestroyAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsAuthenticated]

# Editar usuario
class EditarUsuarioView(generics.UpdateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioEdicionAdminSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.get_queryset().get(id=self.kwargs["pk"])

    def update(self, request, *args, **kwargs):
        if request.user.rol != 'ADMIN':
            return Response({'detail': 'No autorizado. Solo administradores pueden editar usuarios.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)


# recuperación de contraseña 


class SolicitarRecuperacionPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'El correo electrónico es obligatorio'}, status=400)

        Usuario = get_user_model()
        try:
            user = Usuario.objects.get(email=email)
        except Usuario.DoesNotExist:
            return Response({'error': 'No se encontró un usuario con ese correo'}, status=404)

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        url_recuperacion = f"http://localhost:3000/restablecer-password/{uid}/{token}"


        send_mail(
            subject='Recuperación de contraseña - VOLECE.CA',
            message=f'Hola {user.first_name},\n\nHaz clic en el siguiente enlace para restablecer tu contraseña:\n\n{url_recuperacion}',
            from_email=None,  
            recipient_list=[user.email],
        )

        return Response({'message': 'Se ha enviado un correo para restablecer tu contraseña.'}, status=200)



# Restablecer contraseña
Usuario = get_user_model()

class RestablecerPasswordView(APIView):
    def post(self, request):
        #print("DEBUG:", request.data) # utilizado para imprimir uid, token y password para correcto funcionamiento
        uid = request.data.get('uid')
        token = request.data.get('token')
        password = request.data.get('password')

        if not uid or not token or not password:
            return Response({'error': 'Datos incompletos.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            uid_decoded = urlsafe_base64_decode(uid).decode()
            user = get_user_model().objects.get(pk=uid_decoded)
        except Exception:
            return Response({'error': 'Usuario inválido.'}, status=status.HTTP_400_BAD_REQUEST)

        if not default_token_generator.check_token(user, token):
            return Response({'error': 'Token inválido o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(password)
        user.save()

        return Response({'message': 'Contraseña restablecida correctamente.'}, status=status.HTTP_200_OK)

#Lista de transportistas

class ListaTransportistas(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        Usuario = get_user_model()
        transportistas = Usuario.objects.filter(rol='TRANSP')
        data = [
            {
                'id': user.id,
                'nombre': user.first_name,
                'apellido': user.last_name,
            }
            for user in transportistas
        ]
        return Response(data)


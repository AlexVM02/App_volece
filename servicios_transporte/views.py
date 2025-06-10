from rest_framework import generics, permissions
from .models import SolicitudServicio
from .serializers import SolicitudServicioSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


# Crear una nueva solicitud de servicio
class CrearSolicitudServicioView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = SolicitudServicioSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(cliente=self.request.user)


# Listar solicitudes de servicio del cliente
class ListaSolicitudesClienteView(generics.ListAPIView):
    serializer_class = SolicitudServicioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SolicitudServicio.objects.filter(cliente=self.request.user).order_by('-fecha_creacion')

# Listar todas las solicitudes de servicio (solo para admins)
class ListaSolicitudesAdminView(generics.ListAPIView):
    queryset = SolicitudServicio.objects.all().order_by('-fecha_creacion')
    serializer_class = SolicitudServicioSerializer
    permission_classes = [IsAdminUser]  # Solo admins
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'cliente']
    search_fields = ['cliente__username']

# Detalle y actualización de una solicitud de servicio (solo para admins)
class SolicitudDetailView(generics.RetrieveUpdateAPIView):
    queryset = SolicitudServicio.objects.all()
    serializer_class = SolicitudServicioSerializer
    permission_classes = [IsAdminUser]
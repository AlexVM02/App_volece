
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/usuarios/', include('gestion_usuarios.urls')), # URL para la API de usuarios
    path('api/servicios/', include('servicios_transporte.urls')), # URL para la API de servicios de transporte
    path('api/finanzas/', include('finanzas.urls')),
    path('api/', include('gestion_transporte.api_urls')),
    path('api/', include('gestion_vehiculos.urls')),
    
]

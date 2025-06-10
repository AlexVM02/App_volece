# finanzas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('api/obtener_todas_las_cuotas/', views.obtener_todas_las_cuotas, name='obtener_todas_las_cuotas'),
    path('api/marcar_pago/<int:pk>/', views.MarcarCuotaPagadaView.as_view(), name='marcar_pago'),
    path('api/crear_cuotas_mensuales/', views.CrearCuotasMensualesView.as_view(), name='crear_cuotas_mensuales'),  # Asegúrate de que esta ruta esté bien configurada
]

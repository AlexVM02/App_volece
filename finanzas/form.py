from django import forms
from .models import CuotaMensual

class CuotaMensualForm(forms.ModelForm):
    class Meta:
        model = CuotaMensual
        fields = ['socio', 'mes', 'monto', 'fecha_pago', 'estado']  # Los campos que maneja el formulario
        widgets = {
            'mes': forms.DateInput(attrs={'type': 'month'}),  
        }

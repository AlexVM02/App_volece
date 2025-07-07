from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import BaseUserManager

class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, first_name=None, last_name=None, cedula_ruc=None, rol='CLIENTE', telefono= None, **extra_fields):
        if not email:
            raise ValueError('El usuario debe tener un email')
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            cedula_ruc=cedula_ruc,
            rol=rol,
            telefono=telefono,  
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, first_name=None, last_name=None, cedula_ruc=None, telefono= None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')

        return self.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            cedula_ruc=cedula_ruc,
            rol='ADMIN',
            telefono=telefono,
            
            **extra_fields
        )

class Usuario(AbstractUser):
    ROLES = [
        ('ADMIN', 'Administrador'),
        ('TRANSP', 'Transportista'),
        ('CLIENTE', 'Cliente'),
    ]
    rol = models.CharField(max_length=10, choices=ROLES, default='CLIENTE')
    cedula_ruc = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=10, blank=True, null=False)  

    objects = UsuarioManager()

    REQUIRED_FIELDS = ['first_name', 'last_name', 'cedula_ruc', 'email']

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.get_rol_display()})"

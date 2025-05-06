from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.contrib.auth.models import User

# Modelo Cuenta
class Cuenta(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    nro_cuenta = models.CharField(max_length=20, unique=True, null=True, blank=True)
    def __str__(self):
        return f'Cuenta #{self.id} de {self.usuario.username} - Saldo: {self.saldo}'

# Modelo Movimiento
class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE, related_name='movimientos')
    tipo = models.CharField(max_length=20, choices=[('ingreso', 'Ingreso'), ('egreso', 'Egreso'), ('transferencia', 'Transferencia')])
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)
    descripcion = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.tipo} - {self.monto} - {self.fecha}'

# Modelo Beneficiario
class Beneficiario(models.Model):
    propietario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiarios')
    alias = models.CharField(max_length=100)
    beneficiario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='beneficiado_por')
    nro_cuenta = models.CharField(max_length=20) 

    def __str__(self):
        return f'{self.alias} ({self.nro_cuenta})'


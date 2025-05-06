from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import (
    RegistroView,
    CuentaListView,
    IngresarSaldoView,
    RetirarSaldoView,
    TransferirSaldoView,
    BeneficiarioListCreateView,
    BeneficiarioDeleteView,
    CrearCuentaView,
    MovimientosCuentaView,
    UsuarioActualView,
    BorrarCuentaView,
    BeneficiarioUpdateView,
)


urlpatterns = [
    # Auth
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),

    # Registro
    path('registro/', RegistroView.as_view()),
    path('usuarios/me/', UsuarioActualView.as_view(), name='usuario-actual'),

    # Cuentas
    path('cuentas/', CuentaListView.as_view()),
    path('cuentas/<int:pk>/ingresar/', IngresarSaldoView.as_view()),
    path('cuentas/<int:pk>/retirar/', RetirarSaldoView.as_view()),
    path('cuentas/crear/', CrearCuentaView.as_view(), name='crear-cuenta'),
    path('cuentas/<int:pk>/eliminar/', BorrarCuentaView.as_view(), name='eliminar-cuenta'),
    # Transferencias
    path('transferir/', TransferirSaldoView.as_view(), name='transferir'),


    # Movimientos
    path('cuentas/<int:pk>/movimientos/', MovimientosCuentaView.as_view()),

    # Beneficiarios
    path('beneficiarios/', BeneficiarioListCreateView.as_view()),
    path('beneficiarios/<int:id>/', BeneficiarioDeleteView.as_view(), name='eliminar-beneficiario'),
    path('beneficiarios/<int:id>/editar/', BeneficiarioUpdateView.as_view(), name='editar-beneficiario'),

    
]

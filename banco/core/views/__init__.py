from .registro import RegistroView
from .cuentas import (
    CrearCuentaView,CuentaListView, IngresarSaldoView, RetirarSaldoView, TransferirSaldoView,BorrarCuentaView
)
from .movimientos import  MovimientosCuentaView
from .beneficiarios import BeneficiarioUpdateView,BeneficiarioListCreateView, BeneficiarioDeleteView
from ..models import Beneficiario, Cuenta, Movimiento, User, Movimiento
from .usuarios import UsuarioActualView
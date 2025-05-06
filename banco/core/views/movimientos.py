from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models import Cuenta, Movimiento
from core.serializers import MovimientoSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



class MovimientosCuentaView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            cuenta = Cuenta.objects.get(pk=pk, usuario=request.user)
        except Cuenta.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        movimientos = Movimiento.objects.filter(cuenta=cuenta).order_by('-fecha')
        data = [
            {
                "id": m.id,
                "tipo": m.tipo,
                "monto": m.monto,
                "descripcion": m.descripcion,
                "fecha": m.fecha,
            }
            for m in movimientos
        ]
        return Response(data)

import random
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Cuenta, Movimiento
from decimal import Decimal


class CrearCuentaView(APIView):
    permission_classes = [IsAuthenticated]

    def generar_nro_cuenta_unico(self):
        while True:
            numero = str(random.randint(10000000, 99999999))
            if not Cuenta.objects.filter(nro_cuenta=numero).exists():
                return numero

    def post(self, request):
        try:
            nro_cuenta = self.generar_nro_cuenta_unico()
            cuenta = Cuenta.objects.create(
                usuario=request.user,
                saldo=0,
                nro_cuenta=nro_cuenta
            )
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            print("ERROR AL CREAR CUENTA:", str(e))
            return Response({"error": "No se pudo crear la cuenta"}, status=status.HTTP_400_BAD_REQUEST)


class CuentaListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cuentas = Cuenta.objects.filter(usuario=request.user)
        data = [{"id": c.id, "nro_cuenta": c.nro_cuenta, "saldo": c.saldo} for c in cuentas]
        return Response(data)


class BorrarCuentaView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            cuenta = Cuenta.objects.get(pk=pk, usuario=request.user)
            cuenta.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)



class IngresarSaldoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            cuenta = Cuenta.objects.get(pk=pk, usuario=request.user)
        except Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        monto = request.data.get('monto')
        if not monto:
            return Response({'error': 'Monto requerido'}, status=status.HTTP_400_BAD_REQUEST)

        cuenta.saldo += Decimal(str(monto))
        cuenta.save()

        Movimiento.objects.create(cuenta=cuenta, tipo='ingreso', monto=monto)

        return Response({'mensaje': 'Saldo ingresado correctamente'}, status=status.HTTP_200_OK)



class RetirarSaldoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        try:
            cuenta = Cuenta.objects.get(pk=pk, usuario=request.user)
        except Cuenta.DoesNotExist:
            return Response({'error': 'Cuenta no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        monto = request.data.get('monto')
        if not monto:
            return Response({'error': 'Monto requerido'}, status=status.HTTP_400_BAD_REQUEST)

        if cuenta.saldo < Decimal(str(monto)):
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        cuenta.saldo -= Decimal(str(monto))
        cuenta.save()

        Movimiento.objects.create(cuenta=cuenta, tipo='egreso', monto=monto)

        return Response(status=status.HTTP_200_OK)



class TransferirSaldoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print("[TRANSFERENCIA] Petición recibida:", request.data)

        origen_id = request.data.get('origen_id')
        destino_nro = request.data.get('destino_nro')
        monto = request.data.get('monto')

        if not origen_id or not destino_nro or not monto:
            print("Datos incompletos")
            return Response({'error': 'Datos incompletos'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            origen = Cuenta.objects.get(pk=origen_id, usuario=request.user)

        try:
            print(f"Buscando cuenta destino con nro_cuenta {destino_nro}")
            destino = Cuenta.objects.get(nro_cuenta=destino_nro)
        except Cuenta.DoesNotExist:
            print("Cuenta de destino no encontrada")
            return Response({'error': 'Cuenta de destino no encontrada'}, status=status.HTTP_404_NOT_FOUND)

        if origen.saldo < Decimal(str(monto)):
            print(f"Saldo insuficiente: Saldo actual {origen.saldo}, monto requerido {monto}")
            return Response({'error': 'Saldo insuficiente'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            print("Realizando transferencia...")
            origen.saldo -= Decimal(str(monto))
            destino.saldo += Decimal(str(monto))
            origen.save()
            destino.save()

            Movimiento.objects.create(cuenta=origen, tipo=f"Transferencia Salida a {destino.nro_cuenta}", monto=monto)
            Movimiento.objects.create(cuenta=destino, tipo=f"Transferencia Entrada de {origen.nro_cuenta}", monto=monto)

            print("Transferencia realizada con éxito")
            return Response(status=status.HTTP_200_OK)
        except Exception as e:
            print("Error al transferir:", str(e))
            return Response({'error': 'Error al realizar la transferencia'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


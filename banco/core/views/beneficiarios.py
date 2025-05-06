from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from core.models import Beneficiario, Cuenta
from core.serializers import BeneficiarioSerializer

class BeneficiarioListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        beneficiarios = Beneficiario.objects.filter(propietario=request.user)
        data = [
            {
                "id": b.id,
                "alias": b.alias,
                "nro_cuenta": b.nro_cuenta
            }
            for b in beneficiarios
        ]
        return Response(data)

    def post(self, request):
        try:
            alias = request.data.get('alias')
            nro_cuenta = request.data.get('nro_cuenta')

            print("Alias:", alias)
            print("Nro de cuenta:", nro_cuenta)

            if not alias or not nro_cuenta:
                return Response({"error": "Alias y número de cuenta requeridos"}, status=status.HTTP_400_BAD_REQUEST)

            cuenta = Cuenta.objects.filter(nro_cuenta=nro_cuenta).first()
            if not cuenta:
                return Response({"error": "Cuenta no encontrada"}, status=status.HTTP_400_BAD_REQUEST)

            if Beneficiario.objects.filter(propietario=request.user, nro_cuenta=nro_cuenta).exists():
                return Response({"error": "Este beneficiario ya fue agregado"}, status=status.HTTP_400_BAD_REQUEST)

            Beneficiario.objects.create(
                propietario=request.user,
                beneficiario=cuenta.usuario,
                alias=alias,
                nro_cuenta=nro_cuenta
            )
            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print("ERROR al agregar beneficiario:", str(e))
            return Response({"error": "Error interno al agregar beneficiario"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BeneficiarioDeleteView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BeneficiarioSerializer
    queryset = Beneficiario.objects.all()
    lookup_field = 'id'

    def delete(self, request, *args, **kwargs):
        beneficiario = self.get_object()
        if beneficiario.propietario != request.user:
            return Response({"error": "No tienes permiso para eliminar este beneficiario"}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)


class BeneficiarioUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, id):
        try:
            alias = request.data.get('alias')
            if not alias:
                return Response({"error": "El alias es requerido"}, status=status.HTTP_400_BAD_REQUEST)

            beneficiario = Beneficiario.objects.get(id=id, propietario=request.user)
            beneficiario.alias = alias
            beneficiario.save()
            return Response({"mensaje": "Alias actualizado correctamente"})
        except Beneficiario.DoesNotExist:
            return Response({"error": "Beneficiario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
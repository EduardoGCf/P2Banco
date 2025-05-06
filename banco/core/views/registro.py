import random
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import Cuenta

class RegistroView(APIView):
    def post(self, request):
        data = request.data
        print("Datos recibidos:", data)

        try:
            username = data.get('username')
            password = data.get('password')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            id = data.get('ci')
            if not all([username, password, first_name, last_name, id]):
                print("Campos faltantes")
                return Response({'error': 'Faltan campos requeridos'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(username=username).exists():
                print("Usuario ya existe:", username)
                return Response({'error': 'El nombre de usuario ya existe'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(id=id).exists():
                print("CI ya existe:", id)
                return Response({'error': 'El número de CI ya existe'}, status=status.HTTP_400_BAD_REQUEST)
            print("Creando usuario...")
            user = User.objects.create_user(
                id=id,
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            print("Usuario creado:", user.username)

            print("Creando cuenta...")
            Cuenta.objects.create(
                usuario=user,
                saldo=0,
                nro_cuenta=str(random.randint(10000000, 99999999))
            )
            print("Cuenta creada")

            return Response(status=status.HTTP_201_CREATED)

        except Exception as e:
            print("ERROR en el registro:", str(e))
            return Response({'error': 'Error al registrar el usuario'}, status=status.HTTP_400_BAD_REQUEST)

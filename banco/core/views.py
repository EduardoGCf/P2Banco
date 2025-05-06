# core/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Cuenta, Movimiento, Beneficiario
from .serializers import CuentaSerializer, MovimientoSerializer, BeneficiarioSerializer

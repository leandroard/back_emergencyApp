from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework import generics, permissions, status, parsers
from .models import EmergencyType, Emergency
from .serializer import EmergenciesTypeSerializer, EmergencySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny



@extend_schema(
    tags=['emergencies'],
    request={
        'multipart/form-data': {
            'type': 'object',
            'properties': {
                'icon': {
                    'type': 'string',
                    'format': 'binary'
                },
                'name': {"type": "string"}
            }
        }
    },
               )
class EmergencyTypeListApi(generics.ListCreateAPIView):
    queryset = EmergencyType.objects.all()
    serializer_class = EmergenciesTypeSerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder



@extend_schema(tags=['emergencies'])
class EmergencyListCreateApi(generics.ListCreateAPIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder


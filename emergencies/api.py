from django.db import transaction
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.generics import GenericAPIView
from rest_framework import generics, permissions, status, parsers
from rest_framework.response import Response
import requests
from .models import EmergencyType, Emergency
from .serializer import EmergenciesTypeSerializer, EmergencySerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


def send_post_request(user_id, emergencia_id):
    url = 'http://emergencies-node.dev.byteobe.com/alertas/'  # Reemplaza con la URL correcta
    data = {
        'userId': user_id,
        'alertId': emergencia_id
    }
    try:
        response = requests.post(url, json=data)
        print(response)
        response.raise_for_status()  # Esto levantará una excepción para códigos de estado HTTP 4xx/5xx
    except requests.RequestException as e:
        print(f"Error al realizar la petición POST: {e}")


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
    permission_classes = [IsAuthenticated]




@extend_schema(tags=['emergencies'])
class EmergencyListCreateApi(generics.ListCreateAPIView):
    queryset = Emergency.objects.all()
    serializer_class = EmergencySerializer
    permission_classes = [IsAuthenticated]  # Requiere autenticación para acceder

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()

        send_post_request(request.user.id, instance.id)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

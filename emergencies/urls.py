from django.urls import path
from .api import EmergencyTypeListApi, EmergencyListCreateApi

api_urls = ([
              path('emergencies-type', EmergencyTypeListApi.as_view(), name='emergencies-type'),
            path('emergency', EmergencyListCreateApi.as_view(), name='emergencies')
            ], 'emergencies')

urlpatterns = [

]

from django.urls import path, include
from users.urls import api_urls as users_api_users
from emergencies.urls import api_urls as emergencies_api_urls


api_urls = ([
              path('users/', include(users_api_users , namespace='users')),
              path('emergencies/', include(emergencies_api_urls, namespace='emergencies'))
            ], 'main')

urlpatterns = [

]

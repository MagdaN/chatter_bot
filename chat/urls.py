from django.urls import include, path

from rest_framework import routers

from .views import home
from .viewsets import ChatbotViewSet


app_name = 'chat'

router = routers.DefaultRouter()
router.register(r'chatbot', ChatbotViewSet, basename='chatbot')

urlpatterns = [
    path('', home, name='home'),
    path('api/', include(router.urls)),
]

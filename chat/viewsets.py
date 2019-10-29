from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from chatterbot.ext.django_chatterbot import settings

from .bot import ChatBot
from .serializers import ChatbotSerializer


class ChatbotViewSet(GenericViewSet):

    serializer_class = ChatbotSerializer

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def list(self, request, *args, **kwargs):
        return Response({
            'name': self.chatterbot.name
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.data['text']

        if 'in_response_to' in serializer.data:
            additional = {
                'in_response_to': serializer.data['in_response_to']
            }
        else:
            additional = {}

        response = self.chatterbot.get_response(text, additional_response_selection_parameters=additional)
        return Response(response.serialize(), status=200)

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
            "id": None,
            "text": "How can I help you?",
            "persona": "bot:ChatBot"
        })

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.data['text']
        parameters = {
            'persona__startswith': 'bot:'
        }

        if 'in_response_to' in serializer.data:
            parameters['in_response_to'] = serializer.data['in_response_to']

        response = self.chatterbot.get_response(text, additional_response_selection_parameters=parameters)
        return Response(response.serialize(), status=200)

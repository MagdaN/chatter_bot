import json

from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from chatterbot import ChatBot
from chatterbot.ext.django_chatterbot import settings
from chatterbot.conversation import Statement

# from .bot import ChatBot
from .serializers import ChatbotSerializer


class ChatbotViewSet(GenericViewSet):

    serializer_class = ChatbotSerializer

    chatterbot = ChatBot(**settings.CHATTERBOT)

    def list(self, request, *args, **kwargs):
        response = Statement(text='How can I help you?', persona='bot:ChatBot')

        # (re-)init session
        request.session['texts'] = json.dumps([])

        return Response(response.serialize(), status=200)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        text = serializer.data['text']
        session_texts = json.loads(request.session['texts'])

        response = self.chatterbot.get_response(text, additional_response_selection_parameters={
            'session_texts': session_texts
        })

        # only add text to session if it was a proper response
        if response.confidence > 0:
            session_texts.append(response.text)
            request.session['texts'] = json.dumps(session_texts)

        return Response(response.serialize(), status=200)

import importlib

from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Statement
from .serializers import StatementCreateSerializer, StatementSerializer


class ChatbotViewSet(GenericViewSet):

    def get_serializer_class(self):
        if self.action == 'create':
            return StatementCreateSerializer
        else:
            return StatementSerializer

    def get_logic_adapter_class(self):
        module_name, class_name = settings.LOGIC_ADAPTER.rsplit('.', 1)
        return getattr(importlib.import_module(module_name), class_name)

    def list(self, request, *args, **kwargs):
        statement = {
            'id': None,
            'request': None,
            'response': 'How can I help you?',
        }

        serializer = StatementSerializer(statement)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = StatementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        logic_adapter_class = self.get_logic_adapter_class()
        logic_adapter = logic_adapter_class()

        in_response_to = serializer.data.get('in_response_to')
        request = serializer.data.get('request')
        if in_response_to is not None:
            parent = Statement.objects.get(pk=in_response_to)
        else:
            parent = None

        # filter a statement that respond to the last statement
        responses = Statement.objects.filter(parent=parent)
        response = logic_adapter.process(request, responses)

        if not response:
            response = {
                'id': in_response_to,
                'request': None,
                'response': 'Sorry, I don\'t know what that means.',
            }

        # return the first statement
        serializer = StatementSerializer(response)
        return Response(serializer.data)

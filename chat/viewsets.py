import importlib
import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .models import Statement
from .serializers import StatementCreateSerializer, StatementSerializer

logger = logging.getLogger(__name__)


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
            'response': settings.RESPONSES.get('initial'),
        }

        serializer = StatementSerializer(statement)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = StatementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        request_text = serializer.data.get('request')
        in_response_to = serializer.data.get('in_response_to')
        if in_response_to is not None:
            parent = Statement.objects.get(pk=in_response_to)
            parent_response_text = parent.response
        else:
            parent = None
            parent_response_text = None

        logger.debug('request="%s"', request_text)
        logger.debug('parent="%s" (pk=%s)', parent_response_text, in_response_to)

        logic_adapter_class = self.get_logic_adapter_class()
        logic_adapter = logic_adapter_class()

        logger.debug('logic_adapter_class="%s"', logic_adapter_class.__name__)

        # filter a statement that respond to the last statement
        statements = Statement.objects.filter(parent=parent)
        response, similarity = logic_adapter.process(request_text, statements)
        response_text = response.request if response else None

        if similarity < settings.LOGIC_THRESHOLD:
            logger.warning('no response found for request="%s" in response to parent="%s", best guess was request="%s" (similarity=%0.3f)',
                           request_text, parent_response_text, response_text, similarity)

            response = {
                'id': in_response_to,
                'request': None,
                'response': settings.RESPONSES.get('unknown'),
            }

        else:
            logger.info('request="%s" matched "%s" (similarity=%0.3f)', request_text, response_text, similarity)
            logger.debug('response="%s"', response_text)

            if response.redirect:
                try:
                    redirect_statement = Statement.objects.get(request=response.redirect)
                    response.redirect_to = redirect_statement.pk
                    response.redirect_response = redirect_statement.response
                except Statement.DoesNotExist:
                    pass

        # return the first statement
        serializer = StatementSerializer(response)
        return Response(serializer.data)

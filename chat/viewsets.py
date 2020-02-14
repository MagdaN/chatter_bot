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
            'message': None,
            'reply': settings.REPLIES.get('initial'),
        }

        serializer = StatementSerializer(statement)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = StatementCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        message = serializer.data.get('message')
        in_response_to = serializer.data.get('in_response_to')
        if in_response_to is not None:
            parent = Statement.objects.get(pk=in_response_to)
            parent_reply = parent.reply
        else:
            parent = None
            parent_reply = None

        logger.debug('message="%s"', message)
        logger.debug('parent="%s" (pk=%s)', parent_reply, in_response_to)

        logic_adapter_class = self.get_logic_adapter_class()
        logic_adapter = logic_adapter_class()

        logger.debug('logic_adapter_class="%s"', logic_adapter_class.__name__)

        # filter a statement that respond to the last statement
        statements = Statement.objects.filter(parent=parent)
        response, similarity = logic_adapter.process(message, statements)
        response_message = response.message if response else None

        if similarity < settings.LOGIC_THRESHOLD:
            logger.warning('no response found for message="%s" in response to parent="%s", best guess was message="%s" (similarity=%0.3f)',
                           message, parent_reply, response_message, similarity)

            response = {
                'id': in_response_to,
                'message': None,
                'reply': settings.REPLIES.get('unknown'),
            }

        else:
            logger.info('message="%s" matched "%s" (similarity=%0.3f)', message, response_message, similarity)
            logger.debug('reply="%s"', response.reply)

            if not response.children.exists() and not response.conclusion and not response.forward:
                response.conclusion = settings.REPLIES.get('conclusion')

            if response.forward:
                try:
                    response.forward = Statement.objects.get(reference=response.forward)

                    if not response.forward.children.exists() and not response.forward.conclusion and not response.forward.forward:
                        response.forward.conclusion = settings.REPLIES.get('conclusion')

                except Statement.DoesNotExist:
                    pass

        # return the first statement
        serializer = StatementSerializer(response)
        return Response(serializer.data)

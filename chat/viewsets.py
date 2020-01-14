from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
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

        in_response_to = serializer.data.get('in_response_to')
        request = serializer.data.get('request')
        if in_response_to is not None:
            parent = Statement.objects.get(pk=in_response_to)
        else:
            parent = None

        # filter a statement that respond to the last statement and order by similarity
        statements = Statement.objects.filter(parent=parent) \
                              .annotate(similarity=TrigramSimilarity('request', request)) \
                              .filter(similarity__gt=settings.SIMILARITY_THRESHOLD) \
                              .order_by('-similarity')

        if statements:
            statement = statements.first()
        else:
            statement = {
                'id': in_response_to,
                'request': None,
                'response': 'Sorry, I don\'t know what that means.',
            }

        # return the first statement
        serializer = StatementSerializer(statement)
        return Response(serializer.data)

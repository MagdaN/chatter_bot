from django.conf import settings
from rest_framework import serializers

from .models import Statement


class StatementSerializer(serializers.ModelSerializer):

    conclusion = serializers.SerializerMethodField(default=None)

    class Meta:
        model = Statement
        fields = (
            'id',
            'request',
            'response',
            'conclusion'
        )

    def get_conclusion(self, obj):
        if isinstance(obj, Statement) and not obj.children.exists():
            return obj.conclusion or settings.RESPONSES.get('conclusion')
        else:
            return None


class StatementCreateSerializer(serializers.ModelSerializer):

    in_response_to = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Statement
        fields = (
            'request',
            'in_response_to'
        )

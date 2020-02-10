from django.conf import settings
from rest_framework import serializers

from .models import Statement


class StatementSerializer(serializers.ModelSerializer):

    conclusion = serializers.SerializerMethodField(default=None)
    redirect_to = serializers.IntegerField(default=None)
    redirect_response = serializers.CharField(default=None)

    class Meta:
        model = Statement
        fields = (
            'id',
            'request',
            'response',
            'conclusion',
            'redirect_to',
            'redirect_response'
        )

    def get_conclusion(self, obj):
        if isinstance(obj, Statement):
            if not obj.conclusion and not obj.children.exists():
                return settings.RESPONSES.get('conclusion')
            else:
                return obj.conclusion
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

from rest_framework import serializers

from .models import Statement


class StatementSerializer(serializers.ModelSerializer):

    conclusion = serializers.CharField(default=None)
    forward_to = serializers.IntegerField(default=None)
    forward_reply = serializers.CharField(default=None)

    class Meta:
        model = Statement
        fields = (
            'id',
            'message',
            'reply',
            'conclusion',
            'forward_to',
            'forward_reply'
        )


class StatementCreateSerializer(serializers.ModelSerializer):

    in_response_to = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Statement
        fields = (
            'message',
            'in_response_to'
        )

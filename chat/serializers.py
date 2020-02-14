from rest_framework import serializers

from .models import Statement


class ForwardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = (
            'id',
            'reply',
            'conclusion'
        )


class StatementSerializer(serializers.ModelSerializer):

    conclusion = serializers.CharField(default=None)
    forward = ForwardSerializer(default={})

    class Meta:
        model = Statement
        fields = (
            'id',
            'message',
            'reply',
            'conclusion',
            'forward'
        )


class StatementCreateSerializer(serializers.ModelSerializer):

    in_response_to = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Statement
        fields = (
            'message',
            'in_response_to'
        )

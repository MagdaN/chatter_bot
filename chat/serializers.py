from rest_framework import serializers

from .models import Statement


class StatementSerializer(serializers.ModelSerializer):

    conclusion = serializers.CharField(default=None)

    class Meta:
        model = Statement
        fields = (
            'id',
            'request',
            'response',
            'conclusion'
        )


class StatementCreateSerializer(serializers.ModelSerializer):

    in_response_to = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Statement
        fields = (
            'request',
            'in_response_to'
        )

from rest_framework import serializers

from .models import Statement


class StatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Statement
        fields = (
            'id',
            'request',
            'response'
        )


class StatementCreateSerializer(serializers.ModelSerializer):

    in_response_to = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Statement
        fields = (
            'request',
            'in_response_to'
        )

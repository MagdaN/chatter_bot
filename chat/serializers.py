from rest_framework import serializers


class ChatbotSerializer(serializers.Serializer):

    previous = serializers.IntegerField(allow_null=True, required=False)
    text = serializers.CharField(required=True)

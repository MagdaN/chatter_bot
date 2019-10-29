from rest_framework import serializers


class ChatbotSerializer(serializers.Serializer):

    in_response_to = serializers.CharField(required=False)
    text = serializers.CharField(required=True)

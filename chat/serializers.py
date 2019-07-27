from rest_framework import serializers


class ChatbotSerializer(serializers.Serializer):

    text = serializers.CharField(required=True)

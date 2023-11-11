from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('content', 'is_agent', 'created_at_formatted')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True)

    class Meta:
        model = Chat
        fields = ('pk', 'messages')

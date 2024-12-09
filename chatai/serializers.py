from django.core.serializers import json
from rest_framework import serializers

from chatai.models import AuthorType, Conversation, ChatMessageModel


class AuthorTypeSerializer(serializers.ModelSerializer):
    is_human = serializers.BooleanField()

    class Meta:
        model = AuthorType
        fields = '__all__'


class ConversationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversation
        fields = '__all__'


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessageModel
        fields = '__all__'


class CreateChatMessageSerializer(serializers.Serializer):
    content = serializers.CharField()

    class Meta:
        fields = ['content']

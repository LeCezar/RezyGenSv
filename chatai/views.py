from django.db.models import Prefetch
from django.shortcuts import render
from django.template.defaultfilters import title
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from chatai.models import AuthorType, Conversation, ChatMessageModel
from chatai.serializers import AuthorTypeSerializer, ConversationSerializer, ChatMessageSerializer, \
    CreateChatMessageSerializer
from chatai.services import MessageService


# Create your views here.


class AuthorTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuthorType.objects.all()
    serializer_class = AuthorTypeSerializer


class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer

    def get_queryset(self):
        message_prefetch = Prefetch(
            'chatmessagemodel_set',
            queryset=ChatMessageModel.objects.order_by('id')[:1],
            to_attr='first_message'
        )

        return Conversation.objects.prefetch_related(message_prefetch)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)

        for conversation in serializer.data:
            conversation_obj = queryset.get(id=conversation['id'])
            first_message = getattr(conversation_obj, 'first_message', None)
            conversation['first_message'] = (
                ChatMessageSerializer(first_message[0], context=self.get_serializer_context()).data['content']
                if first_message else None
            )

        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def messages(self, request, pk=None):
        conversation = self.get_object()
        chat_messages = ChatMessageSerializer(ChatMessageModel.objects.filter(conversation=conversation), many=True)
        return Response(chat_messages.data)

    @action(detail=True, methods=['post'])
    def add_message(self, request, pk=None):
        conversation = self.get_object()
        message_content = CreateChatMessageSerializer(data=request.data)

        if message_content.is_valid():
            try:
                user_message, response_message = MessageService.add_message_and_generate_response(conversation,
                                                                                                  message_content.data[
                                                                                                      "content"])

                if conversation.chatmessagemodel_set.count() == 2:
                    new_title = MessageService.get_new_title_based_on_first_messages(conversation)
                    if new_title:
                        conversation.title = new_title
                        conversation.save()
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

            user_message_serializer = ChatMessageSerializer(user_message)
            response_message_serializer = ChatMessageSerializer(response_message)

            return Response({
                'user_message': user_message_serializer.data,
                'response_message': response_message_serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response(message_content.errors, status=status.HTTP_400_BAD_REQUEST)

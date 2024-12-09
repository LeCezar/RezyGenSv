from django.db import transaction
from llama_index.core.base.llms.types import ChatMessage, MessageRole
from llama_index.llms.anthropic import Anthropic

from chatai.admin import ANTHROPIC_API_KEY
from chatai.models import Conversation, ChatMessageModel, AuthorType

anthropic_llm = Anthropic(
    api_key=ANTHROPIC_API_KEY,
    model="claude-3-haiku-20240307",
)


class MessageService:
    @staticmethod
    def get_new_title_based_on_first_messages(conversation: Conversation):
        messages = conversation.chatmessagemodel_set.all()
        if messages.count() < 2:
            return None

        first_message = messages[0].content
        response = messages[1].content

        if first_message:
            return MessageService._generate_title_based_on_messages(first_message, response)
        else:
            return None

    @staticmethod
    def add_message_and_generate_response(conversation: Conversation, content: str):
        with transaction.atomic():
            # Create the user message
            user_message = ChatMessageModel.objects.create(
                conversation=conversation,
                author=AuthorType.objects.get(name=AuthorType.PossibleTypes.USER),
                content=content
            )

            # Determine the content of the automated response
            author, response_content = MessageService._generate_response(conversation)

            # Create the response message with the author "ANTHROPIC"
            try:
                author_checked = AuthorType.objects.get(name=author)
            except AuthorType.DoesNotExist:
                raise ValueError("Author 'ANTHROPIC' does not exist.")

            response_message = ChatMessageModel.objects.create(
                author=author_checked,
                conversation=conversation,
                content=response_content
            )

            return user_message, response_message

    @staticmethod
    def _generate_response(conversation: Conversation):
        message_history = conversation.chatmessagemodel_set.all().order_by('id')
        message_history_parsed = [ChatMessage(
            role=MessageService._get_role_from_author(msg.author),
            content=msg.content
        ) for msg in message_history]

        response_msg = anthropic_llm.chat(messages=message_history_parsed).message.content

        return [AuthorType.PossibleTypes.ANTHROPIC, response_msg]

    @staticmethod
    def _generate_title_based_on_messages(message: str, response: str):
        prompt = (f"Give me a name for a conversation that starts with the following message: '{message}'"
                  f"and receives the following response: '{response}'."
                  f"\n Make the name maximum 255 characters long, but try and make it as short as possible."
                  f"Respond only with the title, do not include any other information and do not wrap the title in quotes.")
        return anthropic_llm.chat(
            messages=[ChatMessage(role=MessageRole.USER, content=prompt)]
        ).message.content

    @staticmethod
    def _get_role_from_author(author: AuthorType):
        match author.name:
            case AuthorType.PossibleTypes.USER:
                return MessageRole.USER
            case AuthorType.PossibleTypes.OPENAI:
                return MessageRole.ASSISTANT
            case AuthorType.PossibleTypes.ANTHROPIC:
                return MessageRole.ASSISTANT
            case _:
                return MessageRole.ASSISTANT

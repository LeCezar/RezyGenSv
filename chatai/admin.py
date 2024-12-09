from typing import Any

from django.contrib import admin
from llama_index.llms.anthropic import Anthropic
from llama_index.llms.openai import OpenAI

from chatai.models import ChatMessageModel, Conversation

OPEN_AI_API_KEY = ""
ANTHROPIC_API_KEY = ""


# from playground import start_chat
#
# anthropic_llm = Anthropic(
#     api_key=ANTHROPIC_API_KEY,
#     model="claude-3-haiku-20240307",
# )
#
# openai_llm = OpenAI(api_key=OPEN_AI_API_KEY)
#
# if __name__ == '__main__':
#     start_chat(anthropic_llm)


class ChatMessageModelInline(admin.TabularInline):
    model = ChatMessageModel
    extra = 3


class ConversationAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    search_fields = ['title']
    fieldsets = [
        (None, {'fields': ['title']}),
    ]

    inlines = [ChatMessageModelInline]


admin.site.register(Conversation, ConversationAdmin)

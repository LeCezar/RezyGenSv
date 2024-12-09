from django.db import models
from django.utils.translation import gettext_lazy as _
from llama_index.core.base.llms.types import ChatMessage


# Create your models here.

class AuthorType(models.Model):
    class PossibleTypes(models.TextChoices):
        USER = "USER", _("User")
        OPENAI = "OPENAI", _("OpenAI")
        ANTHROPIC = "ANTHROPIC", _("Anthropic")

    name = models.CharField(max_length=20, choices=PossibleTypes.choices, unique=True, primary_key=True)

    def is_human(self):
        return self.name == AuthorType.PossibleTypes.USER

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Conversation(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ChatMessageModel(models.Model):
    author = models.ForeignKey(AuthorType, on_delete=models.CASCADE, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    content = models.TextField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.content

import textwrap

from click import style
from llama_index.core.base.llms.types import ChatMessage
from llama_index.core.llms.function_calling import FunctionCallingLLM


def start_chat(llm: FunctionCallingLLM):
    message_history = []

    print(f"Type exit to exit. You are talking to: {llm.metadata.model_name}")
    while True:
        message = input("You: ")
        if message == "exit":
            break
        else:
            chat_msg = ChatMessage(
                content=message
            )
            message_history.append(chat_msg)
            gen = llm.stream_chat(messages=message_history)
            response = None
            show_author = True
            for r in gen:
                if show_author:
                    print(r.message.role.capitalize(), end=": ")
                    show_author = False
                response = r

            formatted = textwrap.fill(response.message.content, width=120)
            print(formatted)
            message_history.append(response.message)

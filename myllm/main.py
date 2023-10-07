"""

MYLLM Main 🤖

"""

import importlib
import json
from time import sleep

from loguru import logger

from myllm import __version__
from myllm.config import settings


class MyLLM:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        enabled (bool): Whether MyLLM is enabled
        llm (LLM): LLM
        conversation (ConversationChain): Conversation

    Methods:
        get_myllm_info(self)
        chat(self, prompt)
        clear_chat_history(self)

    """

    def __init__(self):
        """
        Initialize the MyLLM object

        Args:
            None
        """

        self.enabled = settings.myllm_enabled
        if not self.enabled:
            return
        self.llm_ai_mode = settings.llm_ai_mode
        provider_module_name = settings.llm_provider
        provider_module = importlib.import_module(provider_module_name)
        provider_class = getattr(provider_module, provider_module_name.split(".")[-1])
        self.provider = provider_class()
        self.model = settings.llm_model
        self.lag = settings.lag
        self.conversation = Conversation()

    async def get_myllm_info(self):
        """
        Get MyLLM information.

        Returns:
            str: A string containing the MyLLM version,
            model, and provider.
        """
        info = f"ℹ️ {type(self).__name__} {__version__}\n"
        info += f"{self.model}\n{str(settings.llm_provider)}"
        return info

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The response from the conversation model.
        """
        try:
            self.conversation.add_message("user", prompt)
            response = await self.provider.create_async(
                model=self.model,
                messages=self.conversation.get_messages(),
            )
            sleep(self.lag)
            self.conversation.add_message("ai", response)
            return f"{settings.llm_prefix} {response}"
        except Exception as error:
            logger.error("No response {}", error)

    async def clear_chat_history(self):
        """
        Clears the chat history
        """
        self.conversation = Conversation()

    async def export_chat_history(self):
        """
        Clears the chat history
        """
        self.conversation.export_messages()

    async def switch_continous_mode(self):
        """ """
        self.llm_ai_mode = not self.llm_ai_mode
        return f"Continous mode {'enabled' if self.llm_ai_mode else 'disabled'}."


class Conversation:
    def __init__(self, max_memory=settings.max_memory):
        self.messages = []
        self.max_memory = max_memory
        self.template = settings.llm_template
        self.add_message("user", self.template)

    def add_message(self, role: str, content: str):
        if len(self.messages) >= self.max_memory:
            self.messages.pop(0)
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

    def export_messages(self):
        with open("history.json", "w") as f:
            json.dump(self.messages, f, indent=4)

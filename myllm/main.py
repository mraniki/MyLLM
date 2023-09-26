"""

MYLLM Main 🤖

"""

import asyncio
import importlib
from time import sleep

import g4f
from g4f import Provider
from loguru import logger

from myllm import __version__
from myllm.config import settings


class MyLLM:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        logger (Logger): Logger
        enabled (bool): Whether MyLLM is enabled
        commands (str): MyLLM commands
        llm (LLM): LLM
        conversation (ConversationChain): Conversation

    Methods:
        get_myllm_info(self)
        get_myllm_help(self)
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
        self.commands = settings.llm_commands
        self.llm_ai_mode = settings.llm_ai_mode
        provider_module_name = settings.llm_provider
        provider_module = importlib.import_module(provider_module_name)
        provider_class = getattr(provider_module, provider_module_name.split(".")[-1])
        self.provider = provider_class()
        self.conversation = Conversation()

    async def get_myllm_help(self):
        """
        Get the help message for MyLLM.

        Returns:
            str: The help message for the `myllm` command.
        """
        return f"{self.commands}\n"

    async def get_myllm_info(self):
        """
        Get MyLLM information.

        Returns:
            str: A string containing the MyLLM version, model, and provider.
        """
        return (
            f"ℹ️ MyLLM v{__version__}\n {settings.llm_model}\n{settings.llm_provider}"
        )

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The  response from the conversation model.
        """
        self.conversation.add_message("user", prompt)
        logger.debug("conversation {}", self.conversation.get_messages())
        response = await self.provider.create_async(
            model=settings.llm_model,
            messages=self.conversation.get_messages(),
        )

        self.conversation.add_message("ai", response)
        sleep(settings.lag)
        if response:
            logger.debug("response received {}", response)
            return response
        else:
            logger.debug("No response from the model")
            return "No response from the model"

    async def clear_chat_history(self):
        """
        Clears the chat history
        """
        self.conversation = Conversation()

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

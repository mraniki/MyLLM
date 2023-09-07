"""
 
MYLLM Main 🤖

"""

import asyncio
import importlib
from typing import Any, List, Mapping, Optional
import nest_asyncio
import g4f
from g4f import Provider
from langchain.chains import ConversationChain
from langchain.llms.base import LLM
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
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

        self.logger = logger
        self.enabled = settings.llm_enabled
        if not self.enabled:
            return
        self.commands = settings.llm_commands
        self.llm_ai_mode = settings.llm_ai_mode
        self.llm = LangLLM()
        self.conversation = None

    async def get_myllm_info(self):
        """
        Get MyLLM information.

        Returns:
            str: A string containing the MyLLM version, model, and provider.
        """
        return (
            f"ℹ️ MyLLM v{__version__}\n {settings.llm_model}\n{settings.llm_provider}"
        )

    async def get_myllm_help(self):
        """
        Get the help message for MyLLM.

        Returns:
            str: The help message for the `myllm` command.
        """
        return f"{self.commands}\n"

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The predicted response from the conversation model.
        """

        if self.conversation is None:
            self.conversation = ConversationChain(
                llm=self.llm,
                # prompt=PromptTemplate(template=settings.llm_template),
                memory=ConversationBufferMemory(),
            )
        return self.conversation.predict(input=prompt)

    async def clear_chat_history(self):
        """
        Clears the chat history by setting the `conversation`
        attribute to an empty string.
        """
        self.conversation = ""

    async def switch_continous_mode(self):
        """ """
        self.llm_ai_mode = not self.llm_ai_mode
        return f"Continous mode {'enabled' if self.llm_ai_mode else 'disabled'}."


class LangLLM(LLM):
    @property
    def _llm_type(self) -> str:
        """
        Returns the type of the _llm_type property.

        :return: A string representing the type of the property.
        :rtype: str
        """
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """
        Calls the ChatCompletion API to generate a response based on the given prompt.

        Args:
            prompt (str): The prompt for the ChatCompletion API.
            stop (Optional[List[str]], optional): A list of strings that,
            if found in the response,
                indicates the response should be truncated. Defaults to None.

        Returns:
            str: The generated response from the ChatCompletion API.
        """

        nest_asyncio.apply()
        provider_module_name = settings.llm_provider
        provider_module = importlib.import_module(provider_module_name)
        provider_class = getattr(provider_module, provider_module_name.split(".")[-1])
        provider = provider_class()

        out = g4f.ChatCompletion.create(
            model=settings.llm_model,
            provider=provider,
            messages=[{"role": "user", "content": prompt}],
        )
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out

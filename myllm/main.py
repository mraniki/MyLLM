"""
 
MYLLM Main 🤖

"""

import asyncio
import importlib
from typing import Any, List, Mapping, Optional

import g4f
from langchain.chains import LLMChain
from langchain.llms.base import LLM
from loguru import logger

from myllm import __version__
from myllm.config import settings


class MyLLM:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        logger (Logger): Logger
        model (str): Model
        enabled (bool): Enabled
        commands (str): Commands

    Methods:
        get_myllm_info(self)
        get_myllm_help(self)
        talk(self, prompt = settings.llm_default_prompt)

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
        self.model = settings.llm_model
        self.provider = importlib.import_module(settings.llm_provider)
        self.commands = settings.llm_commands
        self.llm_continous = settings.llm_continous
        self.chat_history = ""
        self.llm = LangLLM()
        self.chain = None

    async def get_myllm_info(self):
        """
        Retrieves information about MyLLM including
        its version and the model being used.

        :return: A string containing the MyLLM version and the model.
        """
        return f"ℹ️ MyLLM v{__version__}\n {self.model}\n"

    async def get_myllm_help(self):
        """
        Get the help message for MyLLM.

        Returns:
            str: The help message for the `myllm` command.
        """
        return f"{self.commands}\n"

    async def talk(self, prompt=settings.llm_default_prompt):
        """
        Asynchronously initiates a chat with the given prompt.

        Args:
            prompt (str, optional): The prompt to start the chat with.
            Defaults to settings.llm_default_prompt.

        Returns:
            g4f.ChatCompletion: An instance of the g4f.ChatCompletion class
            representing the chat completion.
        """
        self.logger.info(f"Starting chat with prompt: {prompt}")
        return g4f.ChatCompletion.create(
            model=self.model,
            provider=self.provider,
            messages=[{"role": "user", "content": prompt}],
        )

    async def chat(self, prompt):
        """
        Asynchronously chats with the user using the provided prompt.

        Args:
            prompt (str): The prompt to start the conversation with.

        Returns:
            function: The result of calling the `run` method on the `chain` object.
        """
        self.chain = LLMChain(llm=self.llm, prompt={"content": prompt})
        return self.chain.run

    async def continous_mode(self, prompt):
        """ """
        if self.llm_continous:
            self.chat_history = settings.llm_continous_context
            return await self.chat(prompt)

    async def clear_chat_history(self):
        """ """
        self.chat_history = ""

    async def switch_continous_mode(self):
        """ """
        self.llm_continous = not self.llm_continous
        return f"Continous mode {'enabled' if self.llm_continous else 'disabled'}."


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
        out = g4f.ChatCompletion.create(
            model=settings.llm_model,
            provider=importlib.import_module(settings.llm_provider),
            messages=[{"role": "user", "content": prompt}],
        )
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out

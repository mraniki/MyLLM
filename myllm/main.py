"""
 
MYLLM Main 🤖

"""

import asyncio
import importlib
from typing import Any, List, Mapping, Optional

import g4f
from loguru import logger

from langchain.chains import LLMChain
from langchain.llms.base import LLM

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
        Asynchronously initiates a chat with the given prompt
        and keep the history of the chat.

        Args:
            prompt (str, optional): The prompt to start the chat with.

        Returns:
            g4f.ChatCompletion: An instance of the g4f.ChatCompletion class

        """
       # if self.chat_history:
    #        prompt = (
     #           f"{prompt}, To answer, use the following context: {self.chat_history}"
        #    )
    #    self.chat_history = prompt
        LLMChain(llm=self.llm, prompt=prompt)
        return self.chain.run
        #return await self.talk(prompt)

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

# async def talk(
#     self,
#     prompt = settings.llm_default_prompt
#     ):
# return self.llm(prompt)

#     async def topic(
#         self,
#         new_topic=False,
#         prompt = settings.llm_default_prompt
#         ):
#         if new_topic:
#             self.chain = LLMChain(llm=self.llm, prompt=prompt)
#         return self.chain.run



class LangLLM(LLM):

    @property
    def _llm_type(self) -> str:
        return "custom"

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        out = g4f.ChatCompletion.create(
            model = settings.llm_model,
            provider = importlib.import_module(settings.llm_provider),
            messages=[{"role": "user","content": prompt}],)
        if stop:
            stop_indexes = (out.find(s) for s in stop if s in out)
            min_stop = min(stop_indexes, default=-1)
            if min_stop > -1:
                out = out[:min_stop]
        return out


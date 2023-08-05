"""
 LLME Main
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


class MyLLM():
    """
    MyLLM

    """

    def __init__(self):

        self.logger = logger
        self.enabled = settings.llm_enabled
        if not self.enabled:
            return
        self.commands = settings.llm_commands
        self.llm = LangLLM()
        self.chain = None


    async def get_myllm_info(self):
        return (f"ℹ️ MyLLM v{__version__}\n {self.model}\n")

    async def get_myllm_help(self):
        return (f"{self.commands}\n")


    async def talk(
        self,
        prompt = settings.llm_default_prompt
        ):

        return self.llm(prompt)

    async def topic(
        self,
        new_topic=False,
        prompt = settings.llm_default_prompt
        ):
        if new_topic:
            self.chain = LLMChain(llm=self.llm, prompt=prompt)
        return self.chain.run




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
        


 





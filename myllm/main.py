"""
 LLME Main
"""

import asyncio
import importlib
from serpapi import GoogleSearch

import g4f
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
        self.model = settings.llm_model
        self.provider = importlib.import_module(settings.llm_provider)
        self.commands = settings.llm_commands
    
    @property
    def _llm_type(self) -> str:
        return "custom"

    async def get_myllm_info(self):
        return (f"ℹ️ MyLLM v{__version__}\n {self.model}\n")

    async def get_myllm_help(self):
        return (f"{self.commands}\n")

    async def talk(self, prompt = settings.llm_default_prompt):
        """
        This method has been updated to use the GoogleSearch class from the serpapi module instead of the g4f.ChatCompletion.create() method.
        The prompt is used as the query for the GoogleSearch, and the results are returned as a dictionary.
        The API key for the GoogleSearch is obtained from the settings.serp_api_key, which should be stored and used securely.
        """
        search = GoogleSearch({
            "q": prompt, 
            "api_key": settings.serp_api_key
        })
        result = search.get_dict()
        return result

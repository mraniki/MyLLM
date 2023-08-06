"""
 LLME Main
"""

import asyncio
import importlib
from huggingface_hub import hf_hub_download

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
        return g4f.ChatCompletion.create(
            model=self.model,
            provider = self.provider,
            messages=[
                {"role": "user",
                "content": prompt}],)

    def download_model(self, repo_id):
        try:
            hf_hub_download(repo_id=repo_id, filename="config.json")
        except Exception as e:
            self.logger.error(f"Failed to download model from repo {repo_id}: {e}")

    def login(self):
        from huggingface_hub import HfApi
        HfApi().login(token=settings.huggingface_api_token)

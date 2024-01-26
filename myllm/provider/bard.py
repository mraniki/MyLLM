"""
🔗 Google Bard
via https://github.com/dsdanielpark/Bard-API


"""
from time import sleep

from bardapi import Bard
from loguru import logger

from myllm.provider.client import AIClient


class MyLLMBard(AIClient):
    def __init__(self, **kwargs):
        try:
            super().__init__(**kwargs)
            self.client = Bard(token=self.llm_provider_key)
        except Exception as error:
            logger.error("Bard initialization error {}", error)

    async def chat(self, prompt):
        try:
            response = self.client.get_answer(prompt)["content"]
            sleep(self.timeout)
            self.conversation.add_message("ai", response)
            return f"{self.llm_prefix} {response}"
        except Exception as error:
            logger.error("No response {}", error)

"""
🔗 G4F

"""

import importlib
from time import sleep

from loguru import logger

from ._client import AIClient


class G4fHandler(AIClient):
    """
    MyLLM class for G4F

    """

    def __init__(self, **kwargs):
        """
        Initialize the MyLLM object

        Args:
            None
        """
        super().__init__(**kwargs)
        logger.debug("G4F provider initializing")
        self.llm_provider = kwargs.get("llm_provider", None)
        if self.enabled and self.llm_provider:
            provider_module_name = self.llm_provider
            provider_module = importlib.import_module(provider_module_name)
            provider_class = getattr(
                provider_module, provider_module_name.split(".")[-1]
            )
            self.provider = provider_class()
            self.client = self.provider
            logger.info("Provider {} initialized ", self.provider)

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The response from the conversation model.
        """
        self.conversation.add_message("user", prompt)
        response = None
        try:
            response = await self.provider.create_async(
                model=self.llm_model,
                messages=self.conversation.get_messages(),
            )
        except Exception as error:
            logger.error(error)
        sleep(self.timeout)

        logger.debug("response {}", response)
        if response:
            self.conversation.add_message("assistant", response)
            formatted_response = f"{self.llm_prefix} {response} {self.llm_suffix}"
            logger.debug("User: {}, AI: {}", prompt, response)
            return formatted_response

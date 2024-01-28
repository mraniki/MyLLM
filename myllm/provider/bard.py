"""
🔗 Google Bard
via https://github.com/dsdanielpark/Bard-API


"""
from time import sleep

from bardapi import BardCookies
from loguru import logger

from myllm.provider.client import AIClient


class MyLLMBard(AIClient):
    """
    MyLLM class for Bard

    """

    def __init__(self, **kwargs):
        """
        Initializes the object with the given keyword arguments.
        The client is initialized with the given cookie dictionary.
        refer to
        https://github.com/dsdanielpark/Bard-API/blob/main/documents/README_DEV.md#multi-cookie-bard

        Args:
            **kwargs: Variable length keyword arguments.

        Returns:
            None
        """
        try:
            super().__init__(**kwargs)
            self.client = BardCookies(cookie_dict=self.llm_provider_key)
        except Exception as error:
            self.client = None
            logger.error("Bard initialization error {}", error)

    async def chat(self, prompt):
        """
        An asynchronous function that chats with the client.
        It takes a prompt as input.
        It tries to get an answer from the client and
        adds the response to the conversation.
        It returns a formatted response string.
        """
        try:
            response = self.client.get_answer(prompt)["content"]
            sleep(self.timeout)
            logger.debug("response {}", response)
            if response:
                self.conversation.add_message("ai", response)
                return f"{self.llm_prefix} {response}"
        except Exception as error:
            logger.error("No response {}", error)

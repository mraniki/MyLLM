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
            if self.enabled:
                self.client = BardCookies(cookie_dict=self.llm_provider_key)
            else:
                return None
        except Exception as error:
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
            self.conversation.add_message("user", prompt)

            response = self.client.get_answer(prompt)
            logger.debug("response {}", response)
            messages = self.conversation.get_messages()
            logger.debug("messages {}", messages)

            sleep(self.timeout)

            if response:
                response_content = response["content"]
                self.conversation.add_message("ai", response_content)
                formatted_response = f"{self.llm_prefix} {response_content}"
                logger.debug("User: {}, AI: {}", prompt, response_content)
                return formatted_response
            else:
                logger.warning("Received an empty response for prompt: %s", prompt)
        except Exception as error:
            logger.error("No response {}", error)

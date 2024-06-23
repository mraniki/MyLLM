"""
🔗 Groq.com Support

via https://console.groq.com/docs/quickstart

"""

from time import sleep

from groq import Groq
from loguru import logger

from .client import AIClient


class GroqHandler(AIClient):
    """
    MyLLM class for Groq

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """
        try:
            super().__init__(**kwargs)
            if self.enabled:
                self.client = Groq(
                    api_key=self.llm_provider_key,
                )

            else:
                return None
        except Exception as error:
            logger.error("Groq initialization error {}", error)
            return None

    async def chat(self, prompt):
        """
        Asynchronously chats with the client based on the given prompt.

        :param prompt: The prompt for the chat.
        :return: The response from the chat.
        """
        try:
            self.conversation.add_message("user", prompt)
            archived_messages = self.conversation.get_messages()

            response = self.client.chat.completions.create(
                model=self.llm_model,
                messages=archived_messages,
            )
            sleep(self.timeout)
            response_content = response.choices[0].message.content
            self.conversation.add_message("assistant", response_content)
            return f"{self.llm_prefix} {response_content}"

        except Exception as error:
            logger.error("No response {}", error)

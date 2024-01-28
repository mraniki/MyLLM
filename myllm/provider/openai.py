"""
🔗 OpenAI

via https://github.com/openai/openai-python

"""
from time import sleep

from loguru import logger
from openai import AsyncOpenAI

from myllm.provider.client import AIClient


class MyLLMOpenAI(AIClient):
    """
    MyLLM class for OpenAI

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """
        try:
            super().__init__(**kwargs)
            self.client = AsyncOpenAI(
                api_key=self.llm_provider_key,
            )
        except Exception as error:
            self.client = None
            logger.error("OpenAI initialization error {}", error)

    async def chat(self, prompt):
        """
        Asynchronously chats with the client based on the given prompt.

        :param prompt: The prompt for the chat.
        :return: The response from the chat.
        """
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=self.llm_model,
            )
            sleep(self.timeout)
            logger.debug("response {}", response)
            if response:
              filtered_response = response.choices[0].message.content
              self.conversation.add_message("ai", filtered_response)
              return f"{self.llm_prefix} {filtered_response}"
        except Exception as error:
            logger.error("No response {}", error)

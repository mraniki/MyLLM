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
            if self.enabled:
                self.client = AsyncOpenAI(
                    api_key=self.llm_provider_key,
                )
            else:
                self.client = None
        except Exception as error:
            logger.error("OpenAI initialization error {}", error)

    async def chat(self, prompt):
        """
        Asynchronously chats with the client based on the given prompt.

        :param prompt: The prompt for the chat.
        :return: The response from the chat.
        """
        try:
            self.conversation.add_message("user", prompt)

            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": self.conversation.get_messages(),
                    }
                ],
                model=self.llm_model,
            )

            sleep(self.timeout)

            logger.debug("response {}", response)

            if response:
                response_content = response.choices[0].message.content
                self.conversation.add_message("ai", response_content)
                formatted_response = f"{self.llm_prefix} {response_content}"
                logger.debug("User: {}, AI: {}", prompt, response_content)
                return formatted_response
        except Exception as error:
            logger.error("No response {}", error)

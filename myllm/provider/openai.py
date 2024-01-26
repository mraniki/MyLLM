"""
🔗 OpenAI
via https://github.com/openai/openai-python

"""
from time import sleep

from loguru import logger
from openai import AsyncOpenAI

from myllm.provider.client import AIClient


class MyLLMOpenAI(AIClient):
    def __init__(self):
        # super().__init__
        self.client = AsyncOpenAI(
            api_key=self.llm_provider_key,
            model=self.llm_model,
            temperature=self.temperature,
            max_tokens=self.token_limit,
        )

    async def chat(self, prompt):
        try:
            response = await self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )
            sleep(self.timeout)
            self.conversation.add_message("ai", response)
            return f"{self.llm_prefix} {response}"
        except Exception as error:
            logger.error("No response {}", error)

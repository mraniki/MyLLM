"""
🔗 OpenAI and LocalAI Support

via https://github.com/openai/openai-python
via https://localai.io

"""

from time import sleep

from loguru import logger
from openai import OpenAI

from ._client import AIClient


class OpenaiHandler(AIClient):
    """
    MyLLM class for OpenAI and LocalAI

    """

    def __init__(self, **kwargs):
        """
        Initialize the object with the given keyword arguments.

        :param kwargs: keyword arguments
        :return: None
        """

        super().__init__(**kwargs)
        if self.enabled and self.llm_provider_key:
            self.llm_base_url = kwargs.get("llm_base_url", None)
            self.client = OpenAI(
                api_key=self.llm_provider_key, base_url=self.llm_base_url
            )

    async def chat(self, prompt):
        """
        Asynchronously chats with the client based on the given prompt.

        :param prompt: The prompt for the chat.
        :return: The response from the chat.

        """

        self.conversation.add_message("user", prompt)
        archived_messages = self.conversation.get_messages()

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=archived_messages,
        )
        sleep(self.timeout)

        if response_content := response.choices[0].message.content:
            self.conversation.add_message("assistant", response_content)
            return f"{self.llm_prefix} {response_content}"

    async def vision(self, base64_image):
        """
        Asynchronously summarizes the content of
        an image based on the given base64 encoded image string.

        Args:
            base64_image (str): A base64 encoded image string.

        Returns:
            str: A summarized description of the image content.
        """
        # logger.debug("base64_image {}", base64_image)

        response = self.client.chat.completions.create(
            model=self.llm_model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"{self.vision_prompt}",
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            },
                        },
                    ],
                }
            ],
        )
        sleep(self.timeout)
        logger.debug("response {}", response)
        if response_content := response.choices[0].message.content:
            return f"{self.llm_prefix} {response_content}"

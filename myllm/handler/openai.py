"""
🔗 OpenAI and LocalAI Support

via https://github.com/openai/openai-python
via https://localai.io

"""

from time import sleep

from openai import OpenAI

from .client import AIClient


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

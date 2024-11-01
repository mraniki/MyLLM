"""
🔗 Groq.com Support

via https://console.groq.com/docs/quickstart

"""

from time import sleep

from groq import Groq

from ._client import AIClient


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
        super().__init__(**kwargs)
        if self.enabled and self.llm_provider_key:
            self.client = Groq(
                api_key=self.llm_provider_key,
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
            return f"{self.llm_prefix} {response_content} {self.llm_suffix}"

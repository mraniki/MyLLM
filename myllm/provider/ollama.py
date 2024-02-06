# """
# 🔗 Ollama provider
# https://github.com/ollama/ollama


# """

# from myllm.provider.client import AIClient


# class Ollama(AIClient):
#     """
#     MyLLM class for Ollama

#     """

#     def __init__(self, **kwargs):
#         """
#         Initializes the object with the given keyword arguments.

#         Args:
#             **kwargs: Variable length keyword arguments.

#         Returns:
#             None
#         """
#         pass
#         # try:
#         #     super().__init__(**kwargs)
#         #     if self.enabled:
#         #         self.client = Bard(cookie_dict=self.llm_provider_key)
#         #     else:
#         #         return None
#         # except Exception as error:
#         #     logger.error("Bard initialization error {}", error)
#         #     return None

#     async def chat(self, prompt):
#         """
#         An asynchronous function that chats with the client.
#         It takes a prompt as input.
#         It tries to get an answer from the client and
#         adds the response to the conversation.
#         It returns a formatted response string.
#         """
#         pass
#         # try:
#         #     self.conversation.add_message("user", prompt)
#         #     messages = self.conversation.get_messages()
#         #     logger.debug("messages {}", messages)

#         #     response = self.client.get_answer(prompt)
#         #     sleep(self.timeout)
#         #     logger.debug("response {}", response)

#         #     if response:
#         #         response_content = response["content"]
#         #         self.conversation.add_message("assistant", response_content)
#         #         formatted_response = f"{self.llm_prefix} {response_content}"
#         #         logger.debug("User: {}, AI: {}", prompt, response_content)
#         #         return formatted_response
#         #     else:
#         #         logger.warning("Received an empty response for prompt: %s", prompt)
#         # except Exception as error:
#         #     logger.error("No response {}", error)

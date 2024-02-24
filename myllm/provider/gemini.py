# """
# ♊ Google GeminiLLM
# via https://ai.google.dev/tutorials/python_quickstart


# """

# from time import sleep

# import google.generativeai as genai
# from loguru import logger

# from myllm.provider.client import AIClient


# class GeminiLLM(AIClient):
#     """
#     MyLLM class for Bard

#     """

#     def __init__(self, **kwargs):
#         """
#         Initializes the object with the given keyword arguments.
#         

#         Args:
#             **kwargs: Variable length keyword arguments.

#         Returns:
#             None
#         """
#         try:
#             super().__init__(**kwargs)
#             if self.enabled:
#                 self.client = genai.configure(api_key=self.llm_provider_key)
#                 model = self.client.GenerativeModel('gemini-pro')
#             else:
#                 self.client = None
#         except Exception as error:
#             logger.error("Gemini initialization error {}", error)
#             self.client = None

#     async def chat(self, prompt):
#         """
#         An asynchronous function that chats with the client.
#         It takes a prompt as input.
#         It tries to get an answer from the client and
#         adds the response to the conversation.
#         It returns a formatted response string.
#         """
#         try:
#             self.conversation.add_message("user", prompt)
#             messages = self.conversation.get_messages()
#             logger.debug("messages {}", messages)

#             response = self.client.generate_content(prompt)
#             sleep(self.timeout)
#             logger.debug("response {}", response)

#             if response:
#                 response_content = response["content"]
#                 self.conversation.add_message("assistant", response_content)
#                 formatted_response = f"{self.llm_prefix} {response_content}"
#                 logger.debug("User: {}, AI: {}", prompt, response_content)
#                 return formatted_response
#             else:
#                 logger.warning("Received an empty response for prompt: %s", prompt)
#         except Exception as error:
#             logger.error("No response {}", error)

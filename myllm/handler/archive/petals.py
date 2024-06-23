# """
# 🌸 Petals
# Run large language models at home, BitTorrent style
# https://petals.dev


# """

# from time import sleep

# from loguru import logger
# from petals import AutoDistributedModelForCausalLM
# from transformers import AutoTokenizer

# from .client import AIClient


# class PetalsLLM(AIClient):
#     """
#     MyLLM class for Petals

#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """
#         try:
#             super().__init__(**kwargs)
#             if self.enabled:
#                 model_name = self.llm_model or "petals-team/StableBeluga2"
#                 self.client = AutoTokenizer.from_pretrained(model_name)
#                 self.model =
# AutoDistributedModelForCausalLM.from_pretrained(model_name)
#             else:
#                 return None
#         except Exception as error:
#             logger.error("Petals initialization error {}", error)
#             return None

#     async def chat(self, prompt):
#         """
#         Asynchronously chats with the client based on the given prompt.

#         :param prompt: The prompt for the chat.
#         :return: The response from the chat.
#         """
#         try:
#             self.conversation.add_message("user", prompt)
#             archived_messages = self.conversation.get_messages()
#             logger.debug("archived_messages {}", archived_messages)

#             inputs = self.client(archived_messages, return_tensors="pt")["input_ids"]
#             response = self.model.generate(inputs, max_new_tokens=5)
#             sleep(self.timeout)
#             logger.debug("response {}", response)

#             if response:
#                 response_content = self.client.decode(response[0])
#                 logger.debug("response_content {}", response_content)
#                 self.conversation.add_message("assistant", response_content)
#                 formatted_response = f"{self.llm_prefix} {response_content}"
#                 logger.debug("User: {}, AI: {}", prompt, response_content)
#                 return formatted_response
#         except Exception as error:
#             logger.error("No response {}", error)

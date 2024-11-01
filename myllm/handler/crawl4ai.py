# """
# 🔗 CrawlAI Support

# via https://github.com/unclecode/crawl4ai

# """

# from time import sleep

# from crawl4ai import AsyncWebCrawler
# from crawl4ai.extraction_strategy import LLMExtractionStrategy
# from loguru import logger
# from openai import OpenAI

# from ._client import AIClient


# class Crawl4aiHandler(AIClient):
#     """
#     MyLLM class for Crawl4AI

#     """

#     def __init__(self, **kwargs):
#         """
#         Initialize the object with the given keyword arguments.

#         :param kwargs: keyword arguments
#         :return: None
#         """

#         super().__init__(**kwargs)
#         if self.enabled and self.llm_provider_key:
#             self.llm_base_url = kwargs.get("llm_base_url", None)
#             self.client = OpenAI(
#                 api_key=self.llm_provider_key, base_url=self.llm_base_url
#             )

#     async def chat(self, prompt):
#         """
#         Asynchronously chats with the client based on the given prompt.

#         :param prompt: The prompt for the chat.
#         :return: The response from the chat.

#         """

#         self.conversation.add_message("user", prompt)
#         archived_messages = self.conversation.get_messages()

#         response = self.client.chat.completions.create(
#             model=self.llm_model,
#             messages=archived_messages,
#         )
#         sleep(self.timeout)

#         if response_content := response.choices[0].message.content:
#             self.conversation.add_message("assistant", response_content)
#             return f"{self.llm_prefix} {response_content}"

#     async def vision(self, prompt=None):
#         """
#         Asynchronously chats with the client based on the given prompt.

#         :param prompt: The prompt for the chat.
#         :return: The response from the chat.

#         """

#         async with AsyncWebCrawler(verbose=True) as crawler:
#             result = await crawler.arun(
#                 url=self.browse_url,
#                 word_count_threshold=1,
#                 extraction_strategy=LLMExtractionStrategy(
#                     provider="openai/gpt-4o",
#                     api_token=self.llm_provider_key,
#                     # schema=None,
#                     # extraction_type="schema",
#                     instruction=self.vision_prompt,
#                 ),
#                 bypass_cache=True,
#             )
#             logger.debug("result {}", result)
#             return result.extracted_content


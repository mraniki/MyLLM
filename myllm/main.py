"""

MYLLM Main 🤖

"""

from loguru import logger

from myllm import __version__
from myllm.config import settings
from myllm.provider import MyLLMBard, MyLLMG4F, MyLLMOpenAI


class MyLLM:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        enabled (bool): Whether MyLLM is enabled
        llm (LLM): LLM
        conversation (ConversationChain): Conversation

    Methods:
        get_myllm_info(self)
        chat(self, prompt)
        clear_chat_history(self)

    """

    def __init__(self):
        """
        Initialize the MyLLM object

        Args:
            None
        """

        self.enabled = settings.myllm_enabled
        if not self.enabled:
            return
        logger.info("Initializing MyLLM")
        config = settings.myllm
        self.clients = []
        for item in config:
            logger.debug("Client configuration starting: {}", item)
            _config = config[item]
            if item in ["", "template"]:
                continue
            provider = item
            if provider not in ["g4f", "openai", "bard"]:
                logger.warning(
                    f"Skipping client creation for unsupported provider: {provider}"
                )
                continue
            logger.debug("Client provider: {}", provider)
            client = self._create_client(
                llm_library=provider,
                llm_model=_config.get("llm_model"),
                llm_provider=_config.get("llm_provider"),
                llm_provider_key=_config.get("llm_provider_key"),
                max_memory=_config.get("max_memory") or 5,
                timeout=_config.get("timeout") or 10,
                temperature=_config.get("temperature") or 0,
                token_limit=_config.get("token_limit") or 400,
                llm_prefix=_config.get("llm_prefix") or "",
                llm_template=_config.get("llm_template") or "You are an AI assistant.",
            )
            self.clients.append(client)
            logger.debug(f"Loaded {item}")
            if self.clients:
                logger.info(f"Loaded {len(self.clients)} LLM clients")
            else:
                logger.warning("No LLM clients loaded. Verify config")

    def _create_client(self, **kwargs):
        """

        Create a client based on the given protocol.

        Parameters:
            **kwargs (dict): Keyword arguments that
            contain the necessary information for creating the client.
            The "llm_library" key is required.

        Returns:
            client object based on
            the specified protocol.

        """
        logger.debug("Creating client {}", kwargs["llm_library"])
        if kwargs["llm_library"] == "bard":
            return MyLLMBard(**kwargs)
        elif kwargs["llm_library"] == "openai":
            return MyLLMOpenAI(**kwargs)
        else:
            return MyLLMG4F(**kwargs)

    async def get_info(self):
        """
        Retrieves information about the exchange
        and the account.

        :return: A formatted string containing
        the exchange name and the account information.
        :rtype: str
        """
        version_info = f"ℹ️ {type(self).__name__} {__version__}\n"
        client_info = "".join(
            f"🤖 {client.llm_library} {client.llm_model}\n" for client in self.clients
        )
        return version_info + client_info.strip()

    async def get_chats(self, prompt):
        _chats = ["🤖 Chats"]
        for client in self.clients:
            _chats.append(f"\n{await client.chat(prompt)}")
        return "\n".join(_chats)


#     async def get_myllm_info(self):
#         """
#         Get MyLLM information.

#         Returns:
#             str: A string containing the MyLLM version,
#             model, and provider.
#         """
#         info = f"ℹ️ {type(self).__name__} {__version__}\n"
#         info += f"{self.model}\n{str(settings.llm_provider)}"
#         return info

#     async def chat(self, prompt):
#         """
#         Asynchronously chats with the user.

#         Args:
#             prompt (str): The prompt message from the user.

#         Returns:
#             str: The response from the conversation model.
#         """
#         try:
#             self.conversation.add_message("user", prompt)
#             response = await self.provider.create_async(
#                 model=self.model,
#                 messages=self.conversation.get_messages(),
#             )
#             sleep(self.timeout)
#             self.conversation.add_message("ai", response)
#             return f"{settings.llm_prefix} {response}"
#         except Exception as error:
#             logger.error("No response {}", error)

#     async def clear_chat_history(self):
#         """
#         Clears the chat history
#         """
#         self.conversation = Conversation()

#     async def export_chat_history(self):
#         """
#         Clears the chat history
#         """
#         self.conversation.export_messages()

#     async def switch_continous_mode(self):
#         """ """
#         self.llm_ai_mode = not self.llm_ai_mode
#         return f"Continous mode {'enabled' if self.llm_ai_mode else 'disabled'}."


# class Conversation:
#     def __init__(self, max_memory=settings.max_memory):
#         self.messages = []
#         self.max_memory = max_memory
#         self.template = settings.llm_template
#         self.add_message("user", self.template)

#     def add_message(self, role: str, content: str):
#         if len(self.messages) >= self.max_memory:
#             self.messages.pop(0)
#         self.messages.append({"role": role, "content": content})

#     def get_messages(self):
#         return self.messages

#     def export_messages(self):
#         with open("history.json", "w") as f:
#             json.dump(self.messages, f, indent=4)

"""

MYLLM Main 🤖

"""

from loguru import logger

from myllm import __version__
from myllm.config import settings
from myllm.provider import G4FLLM, OpenAILLM


class MyLLM:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        clients (list): List of LLM clients

    Methods:
        _create_client(self, **kwargs)
        get_info(self)
        get_chats(self, prompt)
        export_chat_history(self)
        clear_chat_history(self)

    """

    def __init__(self):
        """
        Initializes the class instance by creating and appending clients
        based on the configuration in `settings.myllm`.
        If `settings.myllm_enabled` is `False`,
        the class will not create any clients.

        Parameters:
            None

        Returns:
            None
        """
        self.enabled = settings.myllm_enabled
        if not self.enabled:
            logger.info("Module is disabled. No clients will be created.")
            return
        self.clients = []
        self.library_mapping = {
            "g4f": G4FLLM,
            "openai": OpenAILLM,
            # Add mappings here for new libraries
        }
        for name, client_config in settings.myllm.items():
            if name in ["", "template"] or not client_config.get("enabled"):
                continue
            try:
                client = self._create_client(**client_config, name=name)
                if client and getattr(client, "client", None):
                    self.clients.append(client)
            except Exception as e:
                logger.error(f"Failed to create client {name}: {e}")

        logger.info(f"Loaded {len(self.clients)} clients")

    def _create_client(self, **kwargs):
        """
        Create a client based on the given protocol.

        Parameters:
            **kwargs (dict): Keyword arguments that
            contain the necessary information for creating the client.
            The "library" key is required.

        Returns:
            client object based on
            the specified protocol.

        """
        library = kwargs.get("llm_library") or kwargs.get("library")
        client_class = self.library_mapping.get(library)

        if client_class is None:
            logger.error(f"library {library} not supported")
            return None

        return client_class(**kwargs)

    async def get_info(self):
        """
        Retrieves information about the exchange
        and the account.

        :return: A formatted string containing
        the exchange name and the account information.
        :rtype: str
        """
        version_info = f"ℹ️ {type(self).__name__} {__version__}\n"
        client_info = "".join(f"🤖 {client.name}\n" for client in self.clients)
        return version_info + client_info.strip()

    async def chat(self, prompt):
        """
        Asynchronously sends the prompt to each client for a response.
        Concatenates the library name with the response if
        multiple clients are present.
        Returns just the response if a single client is available.
        """
        _chats = []
        for client in self.clients:
            data = await client.chat(prompt)
            if data:
                if len(self.clients) > 1:
                    _chats.append(f"{client.name}\n{data}")
                else:
                    return data
        if _chats:
            return "\n".join(_chats)

    async def export_chat_history(self):
        """
        Asynchronous function to export chat history for each
        client in the list of clients.
        Catches any exceptions and logs them using the logger.
        """
        for client in self.clients:
            await client.export_chat_history()

    async def clear_chat_history(self):
        """
        Asynchronously clears the chat history for each
        client in the list of clients.
        """
        for client in self.clients:
            await client.clear_chat_history()

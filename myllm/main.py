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
        Initialize the MyLLM object which supports multiple LLM libraries

        Args:
            None
        """
        try:
            self.enabled = settings.myllm_enabled
            if not self.enabled:
                return
            logger.info("Initializing")
            config = settings.myllm
            self.clients = []
            for name, client_config in config.items():
                if name in ["", "template"] or not client_config.get("enabled"):
                    continue

                logger.debug("Loading: {}", name)
                client = self._create_client(**client_config, name=name)

                if client and getattr(client, 'client', None):
                    self.clients.append(client)
                    logger.debug(f"Loaded {name}")

            if self.clients:
                logger.info(f"Loaded {len(self.clients)} clients")
            else:
                logger.warning("No clients loaded. Verify config")

        except Exception as e:
            logger.error(f"Error initializing: {e}")

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
        try:
            library = kwargs.get("llm_library")
            logger.debug(f"Creating client {library or 'unknown'}")
            if kwargs["llm_library"] == "g4f":
                return G4FLLM(**kwargs)
            elif kwargs["llm_library"] == "openai":
                return OpenAILLM(**kwargs)
            else:
                logger.error(f"library {library} not supported")
                return None
        except Exception as error:
            logger.error(f"An error occurred while creating the client: {error}")
            return None

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

"""

MYLLM Main 🤖

"""

import base64
import importlib

from loguru import logger
from playwright.async_api import async_playwright

from myllm import __version__
from myllm.config import settings


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
        import_chat_history(self)

    """

    def __init__(self):
        """
        Initializes the class instance by creating and appending clients
        based on the configuration in `settings.myllm`.

        Checks if the module is enabled by looking at `settings.myllm_enabled`.
        If the module is disabled, no clients will be created.

        Creates a mapping of library names to client classes.
        This mapping is used to create new clients based on the configuration.

        If a client's configuration exists in `settings.myllm` and its "enabled"
        key is truthy, it will be created.
        Clients are not created if their name is "template" or empty string.

        If a client is successfully created, it is appended to the `clients` list.

        If a client fails to be created, a message is logged with the name of the
        client and the error that occurred.

        Parameters:
            None

        Returns:
            None
        """
        # Check if the module is enabled
        self.enabled = settings.myllm_enabled

        # Set the prefix for AI agents
        self.ai_agent_mode = settings.ai_agent_mode or False
        self.ai_agent_prefix = settings.ai_agent_prefix or ""
        self.ai_agent_suffix = settings.ai_agent_suffix or ""

        # Set the browser settings
        self.browser_url = settings.browser_url or "https://google.com"
        self.browser_headless = settings.browser_headless or True

        # Create a mapping of library names to client classes
        self.client_classes = self.get_all_client_classes()
        # logger.debug("client_classes available {}", self.client_classes)

        if not self.enabled:
            logger.info("Module is disabled. No Client will be created.")
            return
        self.clients = []

        # Create a client for each client in settings.myllm
        for name, client_config in settings.myllm.items():
            if (
                # Skip empty client configs
                client_config is None
                # Skip non-dict client configs
                or not isinstance(client_config, dict)
                # Skip template and empty string client names
                or name in ["", "template"]
                # Skip disabled clients
                or not client_config.get("enabled")
            ):
                continue
                # Create the client
            logger.debug("Creating client {}", name)
            client = self._create_client(**client_config, name=name)
            # If the client has a valid client attribute, append it to the list
            if client and getattr(client, "client", None):
                self.clients.append(client)

        # Log the number of clients that were created
        logger.info(f"Loaded {len(self.clients)} clients")
        if not self.clients:
            logger.warning(
                "No Client were created. Check your settings or disable the module."
            )

    def _create_client(self, **kwargs):
        """
        Create a client based on the given protocol.

        This function takes in a dictionary of keyword arguments, `kwargs`,
        containing the necessary information to create a client. The required
        key in `kwargs` is "library", which specifies the protocol to use for
        communication with the LLM. The value of "library" must match one of the
        libraries supported by MyLLM.

        This function retrieves the class used to create the client based on the
        value of "library" from the mapping of library names to client classes
        stored in `self.client_classes`. If the value of "library" does not
        match any of the libraries supported, the function logs an error message
        and returns None.

        If the class used to create the client is found, the function creates a
        new instance of the class using the keyword arguments in `kwargs` and
        returns it.

        The function returns a client object based on the specified protocol
        or None if the library is not supported.

        Parameters:
            **kwargs (dict): A dictionary of keyword arguments containing the
            necessary information for creating the client. The required key is
            "library".

        Returns:
            A client object based on the specified protocol or None if the
            library is not supported.

        """
        library = kwargs.get("library") or kwargs.get("llm_library") or "g4f"
        return self.client_classes.get(f"{library.capitalize()}Handler", None).__call__(
            **kwargs
        )

    def get_all_client_classes(self):
        """
        Retrieves all client classes from the `myllm.provider` module.

        This function imports the `myllm.provider` module and retrieves
        all the classes defined in it.

        The function returns a dictionary where the keys are the
        names of the classes and the values are the corresponding
        class objects.

        Returns:
            dict: A dictionary containing all the client classes
            from the `myllm.provider` module.
        """
        provider_module = importlib.import_module("myllm.handler")
        return {
            name: cls
            for name, cls in provider_module.__dict__.items()
            if isinstance(cls, type)
        }

    async def get_info(self):
        """
        Retrieves information about the exchange
        and the account.

        :return: A formatted string containing
        the exchange name and the account information.
        :rtype: str
        """
        version_info = (
            f"ℹ️ {type(self).__name__} {__version__}\n AImode {self.ai_agent_mode}\n"
        )
        client_info = "".join(f"🤖 {client.name}\n" for client in self.clients)
        return version_info + client_info.strip()

    async def chat(self, prompt):
        """
        Asynchronously sends the prompt to each client for a response.
        Concatenates the library name with the response if
        multiple clients are present.
        Returns just the response if a single client is available.
        """

        _chats = [
            (
                data
                if len(self.clients) == 1 and not self.ai_agent_mode
                else (
                    f"{self.ai_agent_prefix} {client.name}\n"
                    f"{data} {self.ai_agent_suffix}"
                )
            )
            for client in self.clients
            if (data := await client.chat(prompt)) is not None and data.strip()
        ]

        if _chats:
            return "\n".join(_chats)

    async def vision(self, prompt=None):
        """
        Asynchronously processes a base64-encoded image
        and returns the responses from each client.

        Parameters:
        base64_image (str): A base64-encoded image.

        Returns:
        str: A string containing the responses
        from each client, separated by newlines.

        """
        _chats = []
        for client in self.clients:
            try:
                if prompt is None:
                    data = await client.vision()
                else:
                    data = await client.vision(prompt=prompt)
                if data is not None and data.strip():
                    if len(self.clients) == 1 and not self.ai_agent_mode:
                        _chats.append(data)
                    else:
                        _chats.append(
                            f"{self.ai_agent_prefix} {client.name}\n"
                            f"{data} {self.ai_agent_suffix}"
                        )
            except AttributeError as e:
                logger.error(
                    f"Error processing with {client.name}: {e}. "
                    "Make sure the client has a vision() method."
                )
            except Exception as e:
                logger.error(f"Error processing with {client.name}: {e}")

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

    async def import_chat_history(self):
        """
        Asynchronously clears the chat history for each
        client in the list of clients.
        """
        for client in self.clients:
            await client.import_chat_history()

    async def browse_url(self, url: str = "https://google.com") -> None:
        """
        Browse URL and save a screenshot of the page.
        """
        logger.info("Browsing URL: {}", url)
        if url is None:
            url = self.browser_url
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch(headless=self.browser_headless)
            await browser.new_context(
                locale="en-US",
                timezone_id="America/Los_Angeles",
                device_scale_factor=1,
                screen={"width": 1920, "height": 1080},
                extra_http_headers={
                    "Accept": (
                        "text/html,application/xhtml+xml,"
                        "application/xml;q=0.9,*/*;q=0.8"
                    ),
                    "Accept-Encoding": "gzip, deflate, br",
                    "Accept-Language": "en-GB,en;q=0.9",
                    "Cache-Control": "max-age=0",
                    "Connection": "keep-alive",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "same-origin",
                    "User-Agent": (
                        "Mozilla/5.0 "
                        "(Macintosh; Intel Mac OS X 10_15_7) "
                        "AppleWebKit/605.1.15 (KHTML, like Gecko) "
                        "Version/17.2.1 Safari/605.1.15"
                    ),
                },
            )
            page = await browser.new_page()
            await page.goto(url)
            # await asyncio.sleep(2)
            # await page.mouse.wheel(0, 300)
            screenshot_bytes = await page.screenshot()
            base64_image = base64.b64encode(screenshot_bytes).decode("utf-8")
            await browser.close()
        return await self.vision(base64_image=base64_image)

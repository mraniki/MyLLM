import json
import os

from loguru import logger


class AIClient:
    """

    MyLLM generic client class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        llm (LLM): LLM
        conversation (ConversationChain): Conversation

    Methods:
        chat(self, prompt)
        clear_chat_history(self)
        export_chat_history(self)
        import_chat_history(self)

    """

    def __init__(self, **kwargs):
        """
        Initialize the MyLLM object

        Args:
            None
        """

        logger.info("Initializing Client")
        try:
            self.name = kwargs.get("name", None)
            self.enabled = kwargs.get("enabled", True)
            self.llm_library = kwargs.get("llm_library", None) or kwargs.get(
                "library", None
            )
            self.llm_model = kwargs.get("llm_model", None)
            self.llm_provider = kwargs.get("llm_provider", None)
            self.llm_provider_key = kwargs.get("llm_provider_key", None)
            self.llm_base_url = kwargs.get("llm_base_url", None)
            self.max_memory = kwargs.get("max_memory", 100)
            self.load_history = kwargs.get("load_history", False)
            self.timeout = kwargs.get("timeout", 2)
            self.llm_prefix = kwargs.get("llm_prefix")
            self.history_filename = (
                kwargs.get("history_filename")
                or f"history-{self.name or 'default'}.json"
            )
            self.llm_template = kwargs.get("llm_template")
        except Exception as error:
            logger.error("Client initialization error {}", error)
            return None
        self.conversation = Conversation(
            max_memory=self.max_memory, llm_template=self.llm_template
        )
        self.client = None

    async def chat(self, prompt):
        """
        Asynchronously chats with the user.

        Args:
            prompt (str): The prompt message from the user.

        Returns:
            str: The response from the conversation model.
        """

    async def clear_chat_history(self):
        """
        Clears the chat history
        """
        self.conversation = Conversation()

    async def export_chat_history(self):
        """
        Clears the chat history
        """
        self.conversation.export_messages(self.history_filename)

    async def import_chat_history(self):
        """
        Import chat history
        """
        self.conversation.import_messages(self.history_filename)


class Conversation:
    """
    Conversation class to store and retrieve conversation history.

    Attributes:
        messages (list): list of messages
        max_memory (int): maximum memory
        template (str): template

    Methods:
        add_message(self, role: str, content: str)
        get_messages(self)
        export_messages(self, filename)
        import_messages(self, filename)

    """

    def __init__(self, max_memory=None, llm_template=None):
        """
        Initialize the class with optional max_memory and llm_template parameters.

        :param max_memory: maximum memory
        :param llm_template: LL template
        """
        self.messages = []
        self.max_memory = max_memory
        self.template = llm_template
        if self.template:
            self.add_message("user", self.template)

    def add_message(self, role: str, content: str):
        """
        Adds a message with the specified role and content to the messages list.

        Args:
            role (str): The role of the message.
            content (str): The content of the message.
        """
        if len(self.messages) >= self.max_memory:
            self.messages.pop(0)
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        """
        Return the messages stored in the instance variable.
        """
        return self.messages

    def export_messages(self, filename):
        """
        Export messages to a JSON file.

        Parameters:
            filename (str): the name of the file

        Returns:
            None
        """
        with open(filename, "w") as f:
            json.dump(self.messages, f, indent=4)

    def import_messages(self, filename):
        """
        Import messages from a JSON file

        Parameters:
            filename (str): the name of the file

        Returns:
            None
        """
        if not os.path.exists(filename):
            return
        if self.load_history:
            with open(filename, "r") as f:
                self.messages = json.load(f)

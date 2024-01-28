import json


class AIClient:
    """

    MyLLM class use to initiate a LLM client
    with a given model and a given provider

    Attributes:
        llm (LLM): LLM
        conversation (ConversationChain): Conversation

    Methods:
        chat(self, prompt)
        clear_chat_history(self)
        export_chat_history(self)

    """

    def __init__(
        self,
        enabled=True,
        llm_library=None,
        llm_model=None,
        llm_provider=None,
        llm_provider_key=None,
        max_memory=None,
        timeout=None,
        temperature=None,
        token_limit=None,
        llm_prefix=None,
        llm_template=None,
    ):
        """
        Initialize the MyLLM object

        Args:
            None
        """
        self.enabled = enabled
        self.llm_library = llm_library
        self.llm_model = llm_model
        self.llm_provider = llm_provider
        self.llm_provider_key = llm_provider_key
        self.llm_prefix = llm_prefix
        self.max_memory = max_memory
        self.timeout = timeout
        self.temperature = temperature
        self.token_limit = token_limit
        self.conversation = Conversation(
            max_memory=max_memory, llm_template=llm_template
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
        self.conversation.export_messages()


class Conversation:
    def __init__(self, max_memory=None, llm_template=None):
        """
        Initialize the class with optional max_memory and llm_template parameters.

        :param max_memory: maximum memory
        :param llm_template: LL template
        """
        self.messages = []
        self.max_memory = max_memory
        self.template = llm_template
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

    def get_messages_as_string(self, separator="\n"):
        """
        Returns the messages stored in the instance variable as a single string.

        Args:
            separator (str): The separator to use between messages.

        Returns:
            str: A string representation of the messages.
        """
        messages_str = separator.join(
            f"{message['role']}: {message['content']}" for message in self.messages
        )
        return messages_str

    def export_messages(self):
        """
        Export messages to a JSON file.

        Parameters:
            self: the instance of the class

        Returns:
            None
        """
        with open("history.json", "w") as f:
            json.dump(self.messages, f, indent=4)

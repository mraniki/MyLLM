"""
Provides example for myllm
"""

import asyncio

from myllm import MyLLM


async def main():
    """Main"""
    talky = MyLLM()

    chat = await talky.chat("My name is Jack")
    print(chat)
    # 🐻 Hello Jack, this is Bing. I'm happy to help you with general tasks. 😊

    chat = await talky.chat("tell me who is president of the united states?")
    print(chat)
    # The current president of the United States is **Joe Biden**[^1^][1] [^2^][2].
    # He took office on **January 20, 2021**[^1^][1] [^2^][2].
    # He is the **46th** president of the United States[^2^][2] [^3^][5].

    chat = await talky.chat("what is my name")
    print(chat)
    # 🐻 You told me your name is Jack. Is that correct?

    await talky.export_chat_history()
    # talky.clear_chat_history()


if __name__ == "__main__":
    asyncio.run(main())

"""
Provides example for myllm
"""

import asyncio
import sys
import time

import uvicorn
from fastapi import FastAPI
from loguru import logger

from myllm import MyLLM

logger.remove()
logger.add(sys.stderr, level="DEBUG")


async def main():
    """Main"""
    talky = MyLLM()
    # asyncio.ensure_future(async_foo())
    chat = await talky.chat("My name is Jack")
    logger.info(chat)
    # Hello Jack, it's nice to meet you!
    # I am an AI language model designed to provide helpful responses.
    #  How can I help you today?
    time.sleep(10)
    chat = await talky.chat("tell me who is president of the united states?")
    logger.info(chat)
    # #  As of my latest update, the current
    # # President of the United States is Joe Biden.
    # # He was inaugurated on January 20th, 2021 and
    # # is the 46th President of the United States.
    time.sleep(10)
    chat = await talky.chat("what is my name")
    logger.info(chat)
    #  Your name is Jack, as you mentioned earlier

    talky.conversation.export_messages()


app = FastAPI()


@app.on_event("startup")
async def start():
    """startup"""
    asyncio.create_task(main())


@app.get("/")
def read_root():
    """root"""
    return {"online"}


@app.get("/health")
def health_check():
    """healthcheck"""
    return {"online"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8089)

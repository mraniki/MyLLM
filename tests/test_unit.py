"""
myllm Unit Testing
"""

import os

import pytest

from myllm.config import settings
from myllm.main import MyLLM


@pytest.fixture(scope="session", autouse=True)
def set_test_settings():
    settings.configure(FORCE_ENV_FOR_DYNACONF="testing")


@pytest.mark.asyncio
async def test_dynaconf():
    assert settings.VALUE == "On Testing"


@pytest.fixture(name="talky")
def test_fixture_myllm():
    return MyLLM()


@pytest.mark.asyncio
async def test_get_myllm_info(talky):
    result = await talky.get_info()
    assert result is not None
    assert "ℹ️" in result


@pytest.mark.asyncio
async def test_myllmclient(talky):
    """Init Testing"""
    assert isinstance(talky, MyLLM)
    assert talky.clients is not None
    assert callable(talky.get_info)
    assert callable(talky.chat)
    for llm in talky.clients:
        assert llm is not None
        # assert llm.llm_library is not None
        assert llm.llm_model is not None
        assert llm.llm_provider is not None
        assert llm.conversation is not None
        assert callable(llm.export_chat_history)
        assert callable(llm.clear_chat_history)
        assert callable(llm.import_chat_history)


@pytest.mark.asyncio
async def test_get_chats(talky):
    result = await talky.chat("tell me a story")
    assert result is not None
    found_keywords = [
        keyword for keyword in ["llama", "bing", "openai", "groq"] if keyword in result
    ]
    assert found_keywords


# @pytest.mark.asyncio
# async def test_get_vision(talky):
#     result = await talky.vision("tell me a story")
#     assert result is not None
#     found_keywords = [
#         keyword for keyword in ["llama", "openai", "groq"] if keyword in result
#     ]
#     assert found_keywords


@pytest.mark.asyncio
async def test_export_chat_history(talky):
    await talky.export_chat_history()
    for llm in talky.clients:
        assert os.path.isfile(llm.history_filename)
        assert callable(llm.import_chat_history)


@pytest.mark.asyncio
async def test_import_chat_history(talky):
    for llm in talky.clients:
        llm.load_history = True
    await talky.import_chat_history()
    for llm in talky.clients:
        assert llm.conversation is not None
        assert llm.conversation.import_messages(filename="notafile.json") is None


@pytest.mark.asyncio
async def test_clear_chat_history(talky):
    await talky.clear_chat_history()
    for llm in talky.clients:
        assert not llm.conversation.messages

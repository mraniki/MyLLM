"""
myllm Unit Testing
"""


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


@pytest.fixture(name="llm_client")
def client_fixture(talky):
    for llm in talky.clients:
        if llm.provider == "g4f":
            return llm

@pytest.fixture(name="bard_client")
def bardclient_fixture(talky):
    for llm in talky.clients:
        if llm.provider == "bard":
            return llm

@pytest.fixture(name="openai_client")
def openaiclient_fixture(talky):
    for llm in talky.clients:
        if llm.provider == "openai":
            return llm

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
    assert callable(talky.get_chats)
    for llm in talky.clients:
        assert llm is not None
        assert llm.llm_library is not None
        assert llm.llm_model is not None
        assert llm.llm_provider is not None
        assert llm.Conversation is not None
        assert callable(llm.export_chat_history)
        assert callable(llm.clear_chat_history)
        assert callable(llm.clear_chat_history)


@pytest.mark.asyncio
async def test_get_chats(talky):
    result = await talky.get_chats("tell me a story")
    assert result is not None


@pytest.mark.asyncio
async def test_chat_g4f(llm_client):
    result = await llm_client.chat("tell me a story")
    assert result is not None

@pytest.mark.asyncio
async def test_chat_openai(openai_client):
    result = await openai_client.chat("tell me a story")
    assert result is not None


@pytest.mark.asyncio
async def test_chat_bard(bard_client):
    result = await bard_client.chat("tell me a story")
    assert result is not None

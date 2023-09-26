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


@pytest.mark.asyncio
async def test_get_myllm_help(talky):
    result = await talky.get_myllm_help()
    assert result is not None
    assert "💬" in result

@pytest.mark.asyncio
async def test_get_myllm_info(talky):
    result = await talky.get_myllm_info()
    assert result is not None
    assert "ℹ️" in result

@pytest.mark.asyncio
async def test_clear_chat_history(talky):
    result = await talky.clear_chat_history()
    assert talky.conversation is not None

@pytest.mark.asyncio
async def test_switch_continous_mode(talky):
    assert settings.llm_ai_mode is True
    result = await talky.switch_continous_mode()
    assert result is not None
    assert "Continous" in result
    assert settings.llm_ai_mode is False


@pytest.mark.asyncio
async def test_chat(talky):
    result = await talky.chat("tell me a story")
    assert result is not None

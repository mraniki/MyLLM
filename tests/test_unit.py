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
    

@pytest.mark.asyncio
async def test_myllm():
    talky = MyLLM()
    response = await talky.chat()
    assert response is not None

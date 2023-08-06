import pytest
from myllm.main import MyLLM

def test_talk_method():
    # Create an instance of MyLLM
    myllm = MyLLM()

    # Define a test prompt
    test_prompt = "Test prompt"

    # Call the talk method with the test prompt
    result = myllm.talk(test_prompt)

    # Assert that the result is a dictionary (as the talk method is expected to return a dictionary)
    assert isinstance(result, dict)

    # Assert that the result contains the expected keys (as the talk method is expected to return a dictionary with these keys)
    assert "organic_results" in result
    assert "ads" in result
    assert "knowledge_graph" in result
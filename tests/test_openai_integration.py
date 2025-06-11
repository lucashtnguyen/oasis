"""
Runs only when RUN_OPENAI_TESTS=true *and* OPENAI_API_KEY is set.
Execute with: pytest -q tests/test_openai_integration.py
"""
import pytest
from openai import OpenAI
from config import settings

_skip = not settings.run_openai_tests or not settings.openai_api_key
pytestmark = pytest.mark.skipif(_skip, reason="Integration tests disabled")


def test_chat_completion_smoke() -> None:
    """Minimal round-trip to verify credentials are valid."""
    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "ping"}],
        max_tokens=1,
    )
    assert resp.choices[0].message.content.strip()

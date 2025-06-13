"""Tests for OpenAI client wrapper."""

import openai
from openai.resources.chat.completions import Completions

from stock_advisor.openai_client import OpenAIClient


def test_chat_success(monkeypatch):
    """Chat returns response on first try."""

    def dummy_create(self, **kwargs):
        return {"choices": []}

    monkeypatch.setattr(Completions, "create", dummy_create)
    client = OpenAIClient(api_key="test")
    res = client.chat([{"role": "user", "content": "hi"}])
    assert res == {"choices": []}


def test_chat_retry(monkeypatch):
    """Chat retries on rate limit."""
    calls = []

    class RateLimitError(Exception):
        pass

    def dummy_create(self, **kwargs):
        if not calls:
            calls.append(1)
            raise RateLimitError("rate")
        return {"choices": []}

    monkeypatch.setattr(Completions, "create", dummy_create)
    client = OpenAIClient(api_key="test")
    res = client.chat([{"role": "user", "content": "hi"}], retries=2, backoff=0)
    assert res == {"choices": []}


def test_chat_with_functions(monkeypatch):
    """Chat forwards function calling params."""

    received = {}

    def dummy_create(self, **kwargs):
        received.update(kwargs)
        return {"choices": []}

    monkeypatch.setattr(Completions, "create", dummy_create)
    client = OpenAIClient(api_key="test")
    funcs = [{"name": "fn", "parameters": {"type": "object", "properties": {}}}]
    res = client.chat(
        [{"role": "user", "content": "hi"}],
        functions=funcs,
        function_call={"name": "fn"},
    )
    assert res == {"choices": []}
    assert received["functions"] == funcs
    assert received["function_call"] == {"name": "fn"}

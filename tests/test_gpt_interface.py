"""Tests for gpt_interface module."""

from stock_advisor.api.gpt_interface import interpret_prompt


class DummyClient:
    def chat(self, messages, retries=3, backoff=0.5):  # noqa: D401
        return {"choices": [{"message": {"content": "{}"}}]}


def test_interpret_prompt_happy(monkeypatch):
    """Happy path for prompt parsing."""
    monkeypatch.setattr(
        "stock_advisor.api.gpt_interface.OpenAIClient", lambda: DummyClient()
    )
    result = interpret_prompt("Show me AAPL")
    assert isinstance(result, dict)


def test_interpret_prompt_empty(monkeypatch):
    """Edge case with empty prompt."""
    monkeypatch.setattr(
        "stock_advisor.api.gpt_interface.OpenAIClient", lambda: DummyClient()
    )
    result = interpret_prompt("")
    assert result == {}

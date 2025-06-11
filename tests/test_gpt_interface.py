"""Tests for gpt_interface module."""

import os

import pytest
from stock_advisor.api.gpt_interface import interpret_prompt, FUNCTION_SCHEMA


class DummyClient:
    def chat(
        self, messages, functions=None, function_call=None, retries=3, backoff=0.5
    ):  # noqa: D401
        return {
            "choices": [
                {
                    "message": {
                        "function_call": {
                            "arguments": '{"ticker":"AAPL","timeframe":"1d"}'
                        }
                    }
                }
            ]
        }


def test_interpret_prompt_happy(monkeypatch):
    """Happy path for prompt parsing."""
    monkeypatch.setattr(
        "stock_advisor.api.gpt_interface.OpenAIClient", lambda: DummyClient()
    )
    result = interpret_prompt("Show me AAPL")
    assert result["ticker"] == "AAPL"


def test_interpret_prompt_empty(monkeypatch):
    """Edge case with empty prompt."""
    monkeypatch.setattr(
        "stock_advisor.api.gpt_interface.OpenAIClient", lambda: DummyClient()
    )
    result = interpret_prompt("")
    assert result == {}


@pytest.mark.integration_openai
def test_interpret_prompt_integration(monkeypatch):
    """Call OpenAI if configured."""
    if not (os.getenv("OPENAI_API_KEY") and os.getenv("RUN_OPENAI_TESTS") == "true"):
        pytest.skip("OpenAI tests disabled")
    result = interpret_prompt("Show me MSFT")
    assert "ticker" in result


def test_function_schema_keys():
    assert FUNCTION_SCHEMA["name"] == "get_stock_chart"
    assert "ticker" in FUNCTION_SCHEMA["parameters"]["properties"]

"""Tests for insights module."""

import pandas as pd
from stock_advisor.api.insights import generate_insights


class DummyClient:
    def chat(self, messages):
        return {}


def test_generate_insights(monkeypatch):
    monkeypatch.setattr(
        "stock_advisor.api.insights.OpenAIClient", lambda: DummyClient()
    )
    df = pd.DataFrame({"Close": [10, 20, 30]})
    result = generate_insights(df)
    assert "Latest close: 30" == result


def test_generate_insights_empty(monkeypatch):
    monkeypatch.setattr(
        "stock_advisor.api.insights.OpenAIClient", lambda: DummyClient()
    )
    result = generate_insights(pd.DataFrame())
    assert result == "No data available."

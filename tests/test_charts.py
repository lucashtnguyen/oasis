"""Tests for chart modules."""

import pandas as pd
import plotly.graph_objects as go

from stock_advisor.visuals.chart_line import chart_line
from stock_advisor.visuals.chart_bar import plot_peer_comparison
from stock_advisor.visuals.chart_candlestick import plot_candlestick
from stock_advisor.visuals.chart_volatility import create_volatility_chart


def test_chart_line_smoke(monkeypatch):
    """Smoke test for multi-series line chart."""

    def dummy_fetch(ticker, timeframe, interval):
        return pd.DataFrame({"Close": [1, 2, 3]})

    monkeypatch.setattr("stock_advisor.visuals.chart_line.fetch_prices", dummy_fetch)
    fig = chart_line(["AAPL", "MSFT"], "1d", "1d")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 2


def test_chart_line_empty(monkeypatch):
    """Edge case with empty data."""

    monkeypatch.setattr(
        "stock_advisor.visuals.chart_line.fetch_prices",
        lambda *a, **k: pd.DataFrame(),
    )
    fig = chart_line(["AAPL"], "1d", "1d")
    assert isinstance(fig, go.Figure)


def test_plot_peer_comparison(monkeypatch):
    def dummy_fetch(*args, **kwargs):
        return pd.DataFrame({"Close": [1, 2]})

    monkeypatch.setattr(
        "stock_advisor.visuals.chart_bar.fetch_prices", dummy_fetch
    )
    fig = plot_peer_comparison(["AAPL", "MSFT"], "1mo")
    assert isinstance(fig, go.Figure)
    assert len(fig.data[0].x) == 2


def test_create_volatility_chart_smoke():
    df = pd.DataFrame({("Close", "AAPL"): [1, 2, 3, 4, 5, 6]})
    fig = create_volatility_chart(df, "AAPL")
    assert isinstance(fig, go.Figure)


def test_plot_candlestick(monkeypatch):
    data = pd.DataFrame(
        {
            "Open": [1],
            "High": [2],
            "Low": [1],
            "Close": [1.5],
        }
    )
    monkeypatch.setattr(
        "stock_advisor.visuals.chart_candlestick.fetch_prices",
        lambda *a, **k: data,
    )
    fig = plot_candlestick("AAPL", "1d", "1m")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1

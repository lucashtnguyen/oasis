"""Tests for chart modules."""

import pandas as pd
import plotly.graph_objects as go

from stock_advisor.visuals.chart_line import chart_line
from stock_advisor.visuals.chart_bar import plot_peer_comparison
from stock_advisor.visuals.chart_candlestick import create_candlestick
from stock_advisor.visuals.chart_volatility import create_volatility_chart


def dummy_fetch(ticker, timeframe, interval):
    cols = pd.MultiIndex.from_tuples([("Close", "AAPL"), ("Close", "MSFT")])
    return pd.DataFrame(data=([1, 1], [2, 2], [3, 3]), columns=cols)


def test_chart_line_smoke(monkeypatch):
    """Smoke test for multi-series line chart."""

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

    monkeypatch.setattr("stock_advisor.visuals.chart_bar.fetch_prices", dummy_fetch)
    fig = plot_peer_comparison(["AAPL", "MSFT"], "1mo")
    assert isinstance(fig, go.Figure)
    assert len(fig.data[0].x) == 2


def test_create_volatility_chart_smoke():
    df = pd.DataFrame({("Close", "AAPL"): [1, 2, 3, 4, 5, 6]})
    fig = create_volatility_chart(df, "AAPL")
    assert isinstance(fig, go.Figure)


def test_plot_candlestick(monkeypatch):
    def dummy_fetch_candlestick(ticker, timeframe, interval):
        cols = pd.MultiIndex.from_tuples(
            [("Open", "AAPL"), ("High", "AAPL"), ("Low", "AAPL"), ("Close", "AAPL")]
        )
        return pd.DataFrame(
            data=([1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]), columns=cols
        )

    monkeypatch.setattr(
        "stock_advisor.visuals.chart_candlestick.fetch_prices", dummy_fetch_candlestick
    )
    fig = create_candlestick("AAPL", "1d", "1m")
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 1

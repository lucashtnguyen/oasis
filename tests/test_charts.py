"""Tests for chart modules."""

import pandas as pd
import plotly.graph_objects as go

from stock_advisor.visuals.chart_line import create_line_chart
from stock_advisor.visuals.chart_bar import create_bar_chart
from stock_advisor.visuals.chart_volatility import create_volatility_chart


def test_create_line_chart_smoke():
    """Smoke test for line chart."""
    df = pd.DataFrame({("Close", "AAPL"): [1, 2, 3]})
    fig = create_line_chart(df, "AAPL")
    assert isinstance(fig, go.Figure)


def test_create_line_chart_empty():
    """Edge case with empty data."""
    fig = create_line_chart(pd.DataFrame(), "AAPL")
    assert isinstance(fig, go.Figure)


def test_create_bar_chart_smoke():
    df = pd.DataFrame({"AAPL": [1, 2], "MSFT": [2, 3]})
    fig = create_bar_chart(df)
    assert len(fig.data) == 2


def test_create_volatility_chart_smoke():
    df = pd.DataFrame({("Close", "AAPL"): [1, 2, 3, 4, 5, 6]})
    fig = create_volatility_chart(df, "AAPL")
    assert isinstance(fig, go.Figure)

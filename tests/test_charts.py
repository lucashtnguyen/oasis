"""Tests for chart modules."""

import pandas as pd
import plotly.graph_objects as go

from stock_advisor.visuals.chart_line import create_line_chart


def test_create_line_chart_smoke():
    """Smoke test for line chart."""
    fig = create_line_chart(pd.DataFrame({"Close": [1, 2, 3]}))
    assert isinstance(fig, go.Figure)


def test_create_line_chart_empty():
    """Edge case with empty data."""
    fig = create_line_chart(pd.DataFrame())
    assert isinstance(fig, go.Figure)

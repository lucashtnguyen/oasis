"""Line or candlestick chart generator."""

from __future__ import annotations

import io
import logging

import pandas as pd
import plotly.graph_objects as go
from stock_advisor.api.stock_fetch import fetch_prices

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def chart_line(tickers: list[str], timeframe: str, interval: str) -> go.Figure:
    """Render a line chart overlaying multiple tickers."""
    logger.debug("Creating line chart for %s", tickers)
    fig = go.Figure()
    for tk in tickers:
        data = fetch_prices(tk, timeframe, interval)
        if not data.empty and "Close" in data:
            fig.add_trace(
                go.Scatter(x=data.index, y=data["Close"], mode="lines", name=tk)
            )
    return fig


def create_line_chart(data: pd.DataFrame, ticker: str) -> go.Figure:
    """Backward compatible single-ticker line chart."""
    logger.debug("create_line_chart backward compatibility")
    fig = go.Figure()
    if not data.empty and "Close" in data:
        if isinstance(data.columns, pd.MultiIndex):
            series = data["Close"][ticker]
        else:
            series = data["Close"]
        fig.add_trace(go.Scatter(y=series, mode="lines"))
    return fig

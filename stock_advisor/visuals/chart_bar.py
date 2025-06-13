"""Peer return comparison chart."""

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


def plot_peer_comparison(tickers: list[str], timeframe: str) -> go.Figure:
    """Plot percentage returns for multiple tickers."""
    logger.debug("Creating peer comparison for %s", tickers)
    returns: dict[str, float] = {}
    for tk in tickers:
        data = fetch_prices(tk, timeframe, "1d")
        if not data.empty and "Close" in data:
            start = data["Close"].iloc[0]
            end = data["Close"].iloc[-1]
            if start != 0:
                returns[tk] = (end - start) / start * 100
    fig = go.Figure(go.Bar(x=list(returns.keys()), y=list(returns.values())))
    fig.update_layout(yaxis_title="Return %")
    return fig


def create_bar_chart(data: pd.DataFrame) -> go.Figure:
    """Backward compatible chart from preloaded data."""
    logger.debug("create_bar_chart backward compatibility")
    fig = go.Figure()
    for column in data.columns:
        fig.add_trace(go.Bar(name=column, y=data[column]))
    return fig

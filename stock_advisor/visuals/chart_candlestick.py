"""Interactive candlestick chart."""

from __future__ import annotations

import io
import logging

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


def plot_candlestick(ticker: str, timeframe: str, interval: str) -> go.Figure:
    """Render an interactive OHLC candlestick chart."""
    logger.debug("Creating candlestick for %s", ticker)
    data = fetch_prices(ticker, timeframe, interval)
    fig = go.Figure()
    if not data.empty:
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name=ticker,
            )
        )
        fig.update_layout(xaxis_rangeslider_visible=True)
    return fig

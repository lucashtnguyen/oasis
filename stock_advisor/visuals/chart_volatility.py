"""Drawdown or volatility chart."""

from __future__ import annotations

import io
import logging

import pandas as pd
import plotly.graph_objects as go

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def create_volatility_chart(data: pd.DataFrame) -> go.Figure:
    """Return a volatility chart."""
    logger.debug("Creating volatility chart")
    fig = go.Figure()
    if not data.empty and "Close" in data:
        returns = data["Close"].pct_change().dropna()
        rolling = returns.rolling(window=5).std()
        fig.add_trace(go.Scatter(y=rolling, mode="lines"))
    return fig

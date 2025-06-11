"""Line or candlestick chart generator."""

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


def create_line_chart(data: pd.DataFrame) -> go.Figure:
    """Return a basic line chart."""
    logger.debug("Creating line chart")
    # TODO: build real chart
    fig = go.Figure()
    return fig

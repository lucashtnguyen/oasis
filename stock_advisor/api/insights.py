"""Generate GPT-based insights from stock data."""

from __future__ import annotations

import io
import logging
from typing import Any

import pandas as pd

from stock_advisor.openai_client import OpenAIClient

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

client = OpenAIClient()


def generate_insights(data: pd.DataFrame) -> str:
    """Return a markdown summary of stock trends."""
    logger.debug("Generating insights for data: %s", data.shape)
    # TODO: call GPT for summary
    _ = client
    return "STUB_INSIGHTS"

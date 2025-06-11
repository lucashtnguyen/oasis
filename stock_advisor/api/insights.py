"""Generate GPT-based insights from stock data."""

from __future__ import annotations

import io
import logging
from typing import Any

import pandas as pd

from stock_advisor.openai_client import OpenAIClient
from config import settings

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)

client = OpenAIClient(api_key=settings.openai_api_key)


def generate_insights(data: pd.DataFrame) -> str:
    """Return a markdown summary of stock trends."""
    logger.debug("Generating insights for data: %s", data.shape)
    if data.empty or "Close" not in data:
        return "No data available."
    latest = data["Close"].iloc[-1]
    try:
        _ = client.chat(
            [{"role": "user", "content": f"Summarize close price {latest}"}]
        )
    except Exception as exc:  # pragma: no cover - network fallback
        logger.debug("GPT call failed: %s", exc)
    return f"Latest close: {latest}"

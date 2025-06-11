"""Stock data retrieval utilities."""

from __future__ import annotations

import io
import logging
from typing import Any

import pandas as pd
import yfinance as yf

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def fetch_prices(
    ticker: str,
    timeframe: str = "1mo",
    interval: str = "1d",
) -> pd.DataFrame:
    """Fetch historical OHLC data."""
    logger.debug("Fetching %s timeframe=%s interval=%s", ticker, timeframe, interval)
    try:
        return yf.download(ticker, period=timeframe, interval=interval)
    except Exception as exc:  # pragma: no cover - network fallback
        logger.debug("yfinance failed: %s", exc)
        logger.debug("STUB_ALPHA_VANTAGE")
        return pd.DataFrame()


# Backwards compatibility
fetch_stock_data = fetch_prices

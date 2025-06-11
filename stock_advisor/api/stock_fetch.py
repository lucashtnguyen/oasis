"""Stock data retrieval."""

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


def fetch_stock_data(ticker: str, period: str = "1mo") -> pd.DataFrame:
    """Fetch historical data for a ticker."""
    logger.debug("Fetching data for %s over %s", ticker, period)
    try:
        data = yf.download(ticker, period=period)
    except Exception as exc:  # TODO: narrow exception
        logger.debug("yfinance failed: %s", exc)
        # TODO: implement Alpha Vantage fallback
        return pd.DataFrame()
    return data

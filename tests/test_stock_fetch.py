"""Tests for stock_fetch module."""

import pandas as pd
import pytest

from stock_advisor.api.stock_fetch import fetch_prices


def test_fetch_prices_happy(monkeypatch):
    """Happy path for data fetch."""

    def dummy_download(*args, **kwargs):
        return pd.DataFrame({"Close": [1, 2, 3]})

    monkeypatch.setattr("yfinance.download", dummy_download)
    data = fetch_prices("AAPL", "1d", "1d")
    assert not data.empty


def test_fetch_prices_bad_ticker(monkeypatch):
    """Edge case for bad ticker."""

    def dummy_download(*args, **kwargs):
        raise ValueError("invalid ticker")

    monkeypatch.setattr("yfinance.download", dummy_download)
    data = fetch_prices("BAD", "1d", "1d")
    assert data.empty

"""Tests for CLI module."""

import sys
import pandas as pd
from stock_advisor import __main__


def test_main_calls_fetch(monkeypatch, capsys):
    def dummy_fetch(ticker, period="1mo"):
        return pd.DataFrame({"Close": [1]})

    monkeypatch.setattr(__main__, "fetch_stock_data", dummy_fetch)
    monkeypatch.setattr("sys.argv", ["prog", "AAPL", "1d"])
    __main__.main()
    captured = capsys.readouterr()
    assert "STUB_CLI" in captured.out

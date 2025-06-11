"""Tests for CLI module."""

import sys
import json
from pathlib import Path

import pandas as pd
from stock_advisor import __main__


class DummyFig:
    def write_html(self, path):
        Path(path).write_text("<html>")

    def show(self):
        pass


def test_handle_query_creates_files(tmp_path, monkeypatch):
    def dummy_interpret(q):
        return {
            "ticker": "AAPL",
            "timeframe": "1d",
            "interval": "1d",
            "chart_type": "line",
        }

    monkeypatch.setattr(__main__, "interpret_prompt", dummy_interpret)
    monkeypatch.setattr(
        __main__, "fetch_prices", lambda *a, **k: pd.DataFrame({"Close": [1, 2, 3]})
    )
    monkeypatch.setattr(__main__, "generate_insights", lambda df: "summary")
    monkeypatch.setattr(__main__, "create_line_chart", lambda df: DummyFig())

    html, md = __main__.handle_query(query="test", output_dir=tmp_path)
    assert Path(html).exists()
    assert Path(md).exists()


def test_main_cli(monkeypatch, capsys):
    monkeypatch.setattr(__main__, "handle_query", lambda **kwargs: ("a.html", "a.md"))
    monkeypatch.setattr(
        "sys.argv",
        [
            "prog",
            "--query",
            "Show AAPL",
            "--output_dir",
            "out",
        ],
    )
    __main__.main()
    captured = capsys.readouterr()
    assert "Chart:" in captured.out

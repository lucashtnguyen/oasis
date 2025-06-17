"""Tests for CLI module."""

from pathlib import Path

import pandas as pd
from click.testing import CliRunner
from stock_advisor import __main__
import stock_advisor.api.query


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

    monkeypatch.setattr(stock_advisor.api.query, "interpret_prompt", dummy_interpret)
    monkeypatch.setattr(
        stock_advisor.api.query,
        "fetch_prices",
        lambda *a, **k: pd.DataFrame({"Close": [1, 2, 3]}),
    )
    monkeypatch.setattr(stock_advisor.api.query, "generate_insights", lambda df: "summary")
    monkeypatch.setattr(stock_advisor.api.query, "chart_line", lambda *a, **k: DummyFig())

    html, md = stock_advisor.api.query.handle_query(query="test", output_dir=tmp_path)
    assert Path(html).exists()
    assert Path(md).exists()


def test_main_cli(monkeypatch):
    runner = CliRunner()
    monkeypatch.setattr(__main__, "handle_query", lambda **kwargs: ("a.html", "a.md"))
    result = runner.invoke(__main__.main, ["--query", "Show AAPL", "--output-dir", "out"])
    assert result.exit_code == 0
    assert "Chart:" in result.output

import pandas as pd
from pathlib import Path

from stock_advisor.api.query import handle_query


class DummyFig:
    def write_html(self, path):
        Path(path).write_text("<html>")

    def show(self):
        pass


def _patch_common(monkeypatch):
    monkeypatch.setattr(
        "stock_advisor.api.query.fetch_prices",
        lambda *a, **k: pd.DataFrame(
            {
                "Open": [1],
                "High": [2],
                "Low": [1],
                "Close": [1.5],
            }
        ),
    )
    monkeypatch.setattr(
        "stock_advisor.api.query.generate_insights", lambda df: "summary"
    )


def test_route_single_candlestick(tmp_path, monkeypatch):
    called = {}

    def dummy(fig_name):
        def _inner(*args, **kwargs):
            called[fig_name] = True
            return DummyFig()

        return _inner

    _patch_common(monkeypatch)
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_candlestick", dummy("candle")
    )
    monkeypatch.setattr("stock_advisor.api.query.chart_line", dummy("line"))
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_peer_comparison", dummy("bar")
    )

    handle_query(input_data={"ticker": "AAPL"}, output_dir=tmp_path)
    assert called.get("candle")
    assert not called.get("line")
    assert not called.get("bar")


def test_route_line_introspection(tmp_path, monkeypatch):
    called = {}

    def dummy(fig_name):
        def _inner(*args, **kwargs):
            called[fig_name] = True
            return DummyFig()

        return _inner

    _patch_common(monkeypatch)
    monkeypatch.setattr("stock_advisor.api.query.chart_line", dummy("line"))
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_peer_comparison", dummy("bar")
    )
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_candlestick", dummy("candle")
    )

    handle_query(
        input_data={
            "ticker": "MSFT",
            "compare": "AAPL",
            "timeframe": "1d",
            "interval": "5m",
        },
        output_dir=tmp_path,
    )
    assert called.get("line")
    assert not called.get("bar")
    assert not called.get("candle")


def test_route_general_comparison(tmp_path, monkeypatch):
    called = {}

    def dummy(fig_name):
        def _inner(*args, **kwargs):
            called[fig_name] = True
            return DummyFig()

        return _inner

    _patch_common(monkeypatch)
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_peer_comparison", dummy("bar")
    )
    monkeypatch.setattr("stock_advisor.api.query.chart_line", dummy("line"))
    monkeypatch.setattr(
        "stock_advisor.api.query.plot_candlestick", dummy("candle")
    )

    handle_query(
        input_data={"ticker": "MSFT", "compare": "AAPL"},
        output_dir=tmp_path,
    )
    assert called.get("bar")
    assert not called.get("line")
    assert not called.get("candle")

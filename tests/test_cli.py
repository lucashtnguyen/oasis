import json
import os
from pathlib import Path

import pytest
from click.testing import CliRunner

import stock_advisor.__main__ as main


@pytest.fixture
def runner():
    return CliRunner()


def test_cli_query_happy(tmp_path, monkeypatch, runner):
    called = {}

    def dummy_handle_query(*, query=None, input_data=None, output_dir="output", show=False):
        called["query"] = query
        called["input"] = input_data
        called["output"] = output_dir
        return "chart.html", "summary.md"

    monkeypatch.setattr(main, "handle_query", dummy_handle_query)
    result = runner.invoke(
        main.main,
        ["--query", "Show AAPL", "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0
    assert "chart.html" in result.output
    assert called["query"] == "Show AAPL"
    assert called["output"] == str(tmp_path)


def test_cli_input_json(tmp_path, monkeypatch, runner):
    recorded = {}

    def dummy_handle_query(*, query=None, input_data=None, output_dir="output", show=False):
        recorded["input"] = input_data
        return "c.html", "s.md"

    monkeypatch.setattr(main, "handle_query", dummy_handle_query)
    payload = {"ticker": "AAPL"}
    result = runner.invoke(
        main.main,
        ["--input", json.dumps(payload), "--output-dir", str(tmp_path)],
    )
    assert result.exit_code == 0
    assert recorded["input"] == payload


def test_cli_use_env_toggle(monkeypatch, runner):
    monkeypatch.setenv("PYTHON_DOTENV", "1")

    def dummy_handle_query(*args, **kwargs):
        return "c.html", "s.md"

    monkeypatch.setattr(main, "handle_query", dummy_handle_query)
    result = runner.invoke(main.main, ["--query", "AAPL", "--no-env"])
    assert result.exit_code == 0
    assert "PYTHON_DOTENV" not in os.environ


def test_cli_missing_required(runner):
    result = runner.invoke(main.main, [])
    assert result.exit_code != 0
    assert "--query" in result.output or "--input" in result.output


def test_cli_invalid_json(runner):
    result = runner.invoke(main.main, ["--input", "{bad}"])
    assert result.exit_code != 0
    assert "Invalid JSON" in result.output

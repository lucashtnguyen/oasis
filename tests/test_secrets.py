"""Tests for secrets loader."""

import os
from tempfile import NamedTemporaryFile

from stock_advisor.config.secrets import load_secrets


def test_load_secrets(tmp_path, monkeypatch):
    env_file = tmp_path / "test.env"
    env_file.write_text("TEST_VAR=42")
    monkeypatch.setenv("TEST_VAR", "")
    load_secrets(str(env_file))
    assert os.getenv("TEST_VAR") == "42"


def test_missing_file(monkeypatch):
    monkeypatch.setenv("TEST_VAR", "")
    load_secrets("nonexistent.env")
    assert os.getenv("TEST_VAR") == ""

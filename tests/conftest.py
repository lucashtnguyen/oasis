import os
import pytest


def pytest_configure(config: pytest.Config) -> None:  # pragma: no cover
    config.addinivalue_line("markers", "integration_openai: OpenAI network tests")


def pytest_collection_modifyitems(config: pytest.Config, items):  # pragma: no cover
    if os.getenv("OPENAI_API_KEY") and os.getenv("RUN_OPENAI_TESTS") == "true":
        return
    skip_marker = pytest.mark.skip(reason="OpenAI tests disabled")
    for item in items:
        if "integration_openai" in item.keywords:
            item.add_marker(skip_marker)

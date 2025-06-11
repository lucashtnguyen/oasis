"""GPT prompt interpreter."""

from __future__ import annotations

import io
import logging
from typing import Dict, Any

from stock_advisor.openai_client import OpenAIClient

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


client = OpenAIClient()


def interpret_prompt(prompt: str) -> Dict[str, Any]:
    """Return structured instructions parsed from a prompt."""
    logger.debug("Interpreting prompt: %s", prompt)
    # TODO: implement GPT function-calling
    _ = client
    return {}

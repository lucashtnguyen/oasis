"""GPT prompt interpreter."""

from __future__ import annotations

import io
import logging
import re
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
    if not prompt.strip():
        return {}
    try:
        response = client.chat([{"role": "user", "content": prompt}])
        logger.debug("GPT response: %s", response)
    except Exception as exc:  # pragma: no cover - network fallback
        logger.debug("GPT call failed: %s", exc)
        response = {}
    tickers = re.findall(r"\b[A-Z]{1,5}\b", prompt)
    return {"tickers": tickers, "raw": prompt}

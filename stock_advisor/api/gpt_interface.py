"""GPT prompt interpreter using function-calling."""

from __future__ import annotations

import io
import json
import logging
import re
from typing import Dict, Any

from stock_advisor.openai_client import OpenAIClient
from stock_advisor.config_settings import settings

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


FUNCTION_SCHEMA = {
    "name": "get_stock_chart",
    "parameters": {
        "type": "object",
        "properties": {
            "ticker": {"type": "string"},
            "timeframe": {"type": "string"},
            "interval": {"type": "string"},
            "chart_type": {"type": "string"},
        },
        "required": ["ticker"],
    },
}

client = OpenAIClient(api_key=settings.openai_api_key)


def interpret_prompt(prompt: str) -> Dict[str, Any]:
    """Return structured instructions parsed from a prompt."""
    logger.debug("Interpreting prompt: %s", prompt)
    if not prompt.strip():
        return {}
    try:
        response = client.chat(
            [{"role": "user", "content": prompt}],
            functions=[FUNCTION_SCHEMA],
            function_call={"name": "get_stock_chart"},
        )
        logger.debug("GPT response: %s", response)
        args = (
            response["choices"][0]["message"]
            .get("function_call", {})
            .get("arguments", "{}")
        )
        data = json.loads(args)
    except Exception as exc:  # pragma: no cover - network fallback
        logger.debug("GPT call failed: %s", exc)
        data = {}
    if "ticker" not in data:
        tickers = re.findall(r"\b[A-Z]{1,5}\b", prompt)
        if tickers:
            data["ticker"] = tickers[0]
    return data

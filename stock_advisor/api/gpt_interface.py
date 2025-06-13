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
            "compare": {"type": "string"},
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
            response.choices[0]
            .to_dict()["message"]
            .get("function_call", {})
            .get("arguments", "{}")
        )
        data = json.loads(args)
    except Exception as exc:  # pragma: no cover - network fallback
        logger.debug("GPT call failed: %s", exc)
        data = {}
    tickers = re.findall(r"\b[A-Z]{1,5}\b", prompt)
    if tickers:
        if "ticker" not in data:
            data["ticker"] = tickers[0]
        if (
            len(tickers) > 1
            and "compare" not in data
            and re.search(r"\bvs\b", prompt, re.IGNORECASE)
        ):
            data["compare"] = tickers[1]

    if "timeframe" not in data:
        tf_match = re.search(
            r"last\s*(\d+)\s*(day|days|d|week|weeks|w|month|months|mo|year|years|y)",
            prompt,
            re.IGNORECASE,
        )
        if tf_match:
            num = tf_match.group(1)
            unit = tf_match.group(2).lower()
            tf_map = {
                "day": "d",
                "days": "d",
                "d": "d",
                "week": "wk",
                "weeks": "wk",
                "w": "wk",
                "month": "mo",
                "months": "mo",
                "mo": "mo",
                "year": "y",
                "years": "y",
                "y": "y",
            }
            data["timeframe"] = f"{num}{tf_map.get(unit, unit)}"

    if "interval" not in data:
        iv_match = re.search(
            r"(\d+)\s*(min|minute|minutes|m|hour|hours|h)",
            prompt,
            re.IGNORECASE,
        )
        if iv_match:
            num = iv_match.group(1)
            unit = iv_match.group(2).lower()
            iv_map = {
                "min": "m",
                "minute": "m",
                "minutes": "m",
                "m": "m",
                "hour": "h",
                "hours": "h",
                "h": "h",
            }
            data["interval"] = f"{num}{iv_map.get(unit, unit)}"
    return data

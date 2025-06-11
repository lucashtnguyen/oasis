"""Thin OpenAI API wrapper with retry and backoff."""

from __future__ import annotations

import os
import time
import logging
import io
from typing import Any, Dict, List

import openai

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


class OpenAIClient:
    """Simple client for interacting with OpenAI."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    def chat(self, messages: List[Dict[str, str]], retries: int = 3, backoff: float = 0.5) -> Any:
        """Send a chat completion request."""
        logger.debug("Sending chat request")
        for attempt in range(retries):
            try:
                return openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)  # TODO: refine
            except Exception as exc:  # TODO: narrow exception
                logger.debug("OpenAI request failed: %s", exc)
                time.sleep(backoff * (2 ** attempt))
        raise RuntimeError("OpenAI request failed after retries")

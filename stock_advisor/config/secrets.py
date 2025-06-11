"""Load environment secrets."""

from __future__ import annotations

import io
import logging
import os
from typing import Any

from dotenv import load_dotenv

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def load_secrets(path: str = ".env") -> None:
    """Load environment variables from a file."""
    logger.debug("Loading secrets from %s", path)
    if not os.path.exists(path):
        logger.debug("Env file not found: %s", path)
        return
    load_dotenv(path, override=True)

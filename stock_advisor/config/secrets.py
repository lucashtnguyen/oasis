"""Load environment secrets."""

from __future__ import annotations

import io
import logging
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
    # TODO: handle missing file errors
    load_dotenv(path)

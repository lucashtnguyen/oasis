"""CLI entry point and public query handler."""

from __future__ import annotations

import argparse
import io
import json
import logging
import os

from stock_advisor.api.gpt_interface import interpret_prompt
from stock_advisor.api.stock_fetch import fetch_prices
from stock_advisor.api.insights import generate_insights
from stock_advisor.visuals.chart_line import create_line_chart
from stock_advisor.api.query import handle_query


DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:  # pragma: no cover - debug scaffold
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def main(argv: list[str] | None = None) -> None:
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description="Stock Advisor CLI")
    parser.add_argument("--query", help="Natural language query")
    parser.add_argument("--input", help="JSON input string")
    parser.add_argument("--output_dir", default="output", help="Output directory")
    parser.add_argument("--show", action="store_true", help="Display chart")
    parser.add_argument(
        "--use-env",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Load variables from .env (default) or rely solely on OS env vars.",
    )
    args = parser.parse_args(argv)

    logger.debug("CLI called with %s", args)

    if not args.use_env:
        os.environ.pop("PYTHON_DOTENV", None)

    input_data = None
    if args.input:
        input_data = json.loads(args.input)

    html_path, md_path = handle_query(
        query=args.query,
        input_data=input_data,
        output_dir=args.output_dir,
        show=args.show,
    )

    print(f"Chart: {html_path}\nSummary: {md_path}")


if __name__ == "__main__":
    main()

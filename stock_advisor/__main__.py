"""CLI entry point and public query handler."""

from __future__ import annotations

import argparse
import io
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any

from .api.gpt_interface import interpret_prompt
from .api.stock_fetch import fetch_prices
from .api.insights import generate_insights
from .visuals.chart_line import create_line_chart
from .visuals.chart_bar import create_bar_chart
from .visuals.chart_volatility import create_volatility_chart

DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:  # pragma: no cover - debug scaffold
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def handle_query(
    query: str | None = None,
    input_data: Dict[str, Any] | None = None,
    output_dir: str = "output",
    show: bool = False,
) -> tuple[str, str]:
    """Process a user query or structured input."""
    if query and input_data:
        raise ValueError("Provide either query or input, not both")
    if not (query or input_data):
        raise ValueError("No query or input provided")

    if query:
        params = interpret_prompt(query)
    else:
        params = input_data or {}

    ticker = params.get("ticker") or params.get("tickers", [None])[0]
    timeframe = params.get("timeframe", "1mo")
    interval = params.get("interval", "1d")
    chart_type = params.get("chart_type", "line")

    logger.debug(
        "Handling query for %s timeframe=%s interval=%s chart=%s",
        ticker,
        timeframe,
        interval,
        chart_type,
    )

    data = fetch_prices(ticker, timeframe, interval)

    if chart_type == "bar":
        fig = create_bar_chart(data)
    elif chart_type == "volatility":
        fig = create_volatility_chart(data)
    else:
        fig = create_line_chart(data)

    summary = generate_insights(data)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    slug = f"{ticker}_{timeframe}_{interval}"
    html_path = Path(output_dir) / f"{slug}.html"
    fig.write_html(str(html_path))
    md_path = Path(output_dir) / f"{slug}.md"
    md_path.write_text(summary)
    if show:
        try:  # pragma: no cover - optional UI
            fig.show()
        except Exception as exc:  # pragma: no cover - headless
            logger.debug("fig.show failed: %s", exc)
    return str(html_path), str(md_path)


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

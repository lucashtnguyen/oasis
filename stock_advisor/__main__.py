"""CLI entry point for Stock Advisor."""

import argparse
from .api.stock_fetch import fetch_stock_data

DEBUG = True

import logging
import io

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


def main() -> None:
    """Run the command-line interface."""
    parser = argparse.ArgumentParser(description="Stock Advisor CLI")
    parser.add_argument("ticker", nargs="?", help="Ticker symbol")
    parser.add_argument("period", nargs="?", default="1mo", help="Data period")
    args = parser.parse_args()
    logger.debug("CLI called with %s", args)
    # TODO: implement real CLI behavior
    if args.ticker:
        fetch_stock_data(args.ticker, args.period)
    print("STUB_CLI")


if __name__ == "__main__":
    main()

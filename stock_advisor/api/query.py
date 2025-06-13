import logging
from stock_advisor.api.gpt_interface import interpret_prompt
from stock_advisor.api.insights import generate_insights
from stock_advisor.api.stock_fetch import fetch_prices
from stock_advisor.visuals.chart_bar import plot_peer_comparison
from stock_advisor.visuals.chart_line import chart_line
from stock_advisor.visuals.chart_candlestick import plot_candlestick
from stock_advisor.visuals.chart_volatility import create_volatility_chart


from pathlib import Path
from typing import Any, Dict

logger = logging.getLogger(__name__)


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
    compare = params.get("compare")
    timeframe = params.get("timeframe", "1mo")
    interval = params.get("interval", "1d")
    chart_type = params.get("chart_type")

    logger.debug(
        "Handling query tickers=%s timeframe=%s interval=%s chart=%s",
        [ticker, compare] if compare else [ticker],
        timeframe,
        interval,
        chart_type,
    )

    tickers = [t for t in [ticker, compare] if t]

    if compare and (
        ("timeframe" in params and "interval" in params) or chart_type == "line"
    ):
        fig = chart_line(tickers, timeframe, interval)
    elif chart_type in {"bar", "comparison"} or (
        compare and not ("timeframe" in params and "interval" in params)
    ):
        fig = plot_peer_comparison(tickers, timeframe)
    elif chart_type == "line":
        fig = chart_line(tickers, timeframe, interval)
    else:
        fig = plot_candlestick(ticker, timeframe, interval)

    data = fetch_prices(ticker, timeframe, interval)

    summary = generate_insights(data)

    Path(output_dir).mkdir(parents=True, exist_ok=True)
    slug = f"{'_'.join(tickers)}_{timeframe}_{interval}"
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

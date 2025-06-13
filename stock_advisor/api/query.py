import logging
from stock_advisor.api.gpt_interface import interpret_prompt
from stock_advisor.api.insights import generate_insights
from stock_advisor.api.stock_fetch import fetch_prices
from stock_advisor.visuals.chart_bar import create_bar_chart
from stock_advisor.visuals.chart_line import create_line_chart
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
        fig = create_volatility_chart(data, ticker)
    else:
        fig = create_line_chart(data, ticker)

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

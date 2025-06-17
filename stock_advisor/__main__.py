"""CLI entry point and public query handler."""

from __future__ import annotations

import io
import json
import logging
import os
from pathlib import Path

import click

from stock_advisor.api.query import handle_query


DEBUG = True

logger = logging.getLogger(__name__)
log_buffer = io.StringIO()
if DEBUG:  # pragma: no cover - debug scaffold
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)


@click.command(context_settings={"auto_envvar_prefix": "STOCK_ADVISOR"})
@click.option("--query", type=str, help="Natural language query")
@click.option("--input", "input_json", type=str, help="JSON input string")
@click.option(
    "--output-dir",
    type=click.Path(file_okay=False, path_type=Path),
    default="output",
    help="Output directory",
)
@click.option("--use-env/--no-env", default=True, help="Load .env file")
def main(query: str | None, input_json: str | None, output_dir: Path, use_env: bool) -> None:
    """Run the command-line interface."""
    logger.debug(
        "CLI called with query=%s input=%s output=%s use_env=%s",
        query,
        input_json,
        output_dir,
        use_env,
    )

    if not use_env:
        os.environ.pop("PYTHON_DOTENV", None)

    input_data = None
    if input_json:
        try:
            input_data = json.loads(input_json)
        except json.JSONDecodeError as exc:
            raise click.BadParameter(f"Invalid JSON: {exc}") from exc

    if not (query or input_data):
        raise click.UsageError("Either --query or --input is required")

    html_path, md_path = handle_query(
        query=query,
        input_data=input_data,
        output_dir=str(output_dir),
        show=False,
    )

    click.echo(f"Chart: {html_path}\nSummary: {md_path}")


if __name__ == "__main__":
    main()

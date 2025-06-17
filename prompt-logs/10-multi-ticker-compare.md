# Pull Request #10
**Prompt:**
You are a **Lead Python TDD Engineer**.
Read **`spec.md`**, the existing **`stock_advisor/`** code (including `gpt_interface.py` and `handle_query`), and extend the **visuals** layer to fully support multi-ticker comparisons, time-series introspection, and candlestick charts, integrating smoothly with the function-calling output.

---

### 1 · Update `handle_query`

* Accept an optional `"compare"` parameter from `interpret_prompt()`.
* **Time-series introspection** (e.g. queries like “compare MSFT to AAPL for 1 day, 5 min chart”) **or** explicit `--chart_type line` → route to **`chart_line()`**.
* Explicit `--chart_type bar` or `--chart_type comparison`, **or** compare param without a timeframe/interval introspection phrase → route to **`plot_peer_comparison()`**.
* All other single-ticker requests → route to **`plot_candlestick()`**.

---

### 2 · Enhance visuals modules

* **chart\_line.py** – accept `tickers: list[str]` and overlay multiple series.
* **chart\_bar.py** – implement `plot_peer_comparison(tickers: list[str], timeframe: str) -> Figure` per the bar-plot spec.
* **chart\_candlestick.py** – new module stub code for you to complete below: 

  ```python
  def plot_candlestick(
      ticker: str, timeframe: str, interval: str
  ) -> plotly.graph_objects.Figure:
      """Render an interactive OHLC candlestick chart."""
      # TODO: fetch prices; build fig with go.Candlestick; add range slider
  ```

---

### 3 · Tests & TDD

* Unit tests for `chart_line()`, `plot_peer_comparison()`, and `plot_candlestick()`.
* Mock price fetches for bar and candlestick tests.
* End-to-end tests covering:

  * single-ticker → candlestick
  * line introspection → line
  * general comparison → bar

---

### 4 · Conventions & output

* **Python 3.12**, docstrings only; maintain `DEBUG` + `log_buffer` logging.
* Present changes as **patch-style** blocks for `git apply`, splitting > 300 lines into **Part n/m**.
* Finish with a **Next steps** section (≤ 5 bullets) noting any `# TODO:` or refactoring suggestions.
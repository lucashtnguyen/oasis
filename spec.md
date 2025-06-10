### 1 · Scope & Objectives

1. **Purpose & success metrics**
   This project builds an LLM-assisted tool that fetches and visualizes stock data using structured GPT function-calling. It translates natural language prompts like “Show me NVDA vs AMD for the past 3 months” into charts and narrative insights using `yfinance` and Plotly.
   **Success =** >90% of valid queries produce correct charts + GPT-generated insights within 1s (excluding fetch time).

2. **Core features**

* GPT function-calling to extract ticker(s), time range, and chart type.
* Data fetch via `yfinance`; fallback to Alpha Vantage stub.
* Visual types:

  * Line/candlestick time-series
  * Peer comparison bar chart
  * Drawdown/volatility overlays
* GPT summary of trend/momentum in markdown
* CLI-friendly `.py` module structure

**Definition of done:** Core chart functions and GPT response generator work for all 3 sample queries.

3. **Non-goals**

* No Streamlit or web frontend
* No real-time portfolio analysis or alerts
* No financial advice or risk modelling

---

### 2 · Domain & Data

| Item                 | Detail                                                                                         |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| Primary domain       | Retail investing + LLM-enhanced visualization                                                  |
| Data sources         | `yfinance` (primary); Alpha Vantage stub (fallback)                                            |
| Format               | JSON / CSV; ≤10 KB per request                                                                 |
| Licensing/compliance | [Yahoo Finance TOS](https://legal.yahoo.com/us/en/yahoo/terms/product-atos/index.html); no PII |

---

### 3 · Technical Blueprint

**Language**: Python 3.12
**Architecture**:

```
stock_advisor/
├── __main__.py            # Optional CLI stub
├── api/
│   ├── gpt_interface.py   # Function schema + payload interpreter
│   ├── stock_fetch.py     # yfinance interface + fallback stub
│   └── insights.py        # Summary markdown from chart context
├── visuals/
│   ├── chart_line.py      # Line/candlestick chart generator
│   ├── chart_bar.py       # Peer return comparison
│   └── chart_volatility.py# Drawdown or rolling volatility
├── config/
│   └── secrets.py         # dotenv-based secrets loader
├── tests/
│   ├── test_stock_fetch.py
│   ├── test_charts.py
│   └── test_gpt_interface.py
└── pyproject.toml         # Build metadata + pinned versions
```

**Pinned Dependencies**:

* `openai==1.30.1`
* `pandas==2.2.2`
* `plotly==5.22.0`
* `yfinance==0.2.37`
* `python-dotenv==1.0.1`
* `pytest==8.2.2`

---

### 4 · Coding Standards & Debug Workflow

```python
DEBUG = True
logger = logging.getLogger(__name__)
log_buffer = io.StringIO()

if DEBUG:
    handler = logging.StreamHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)
```

Add `logger.debug(...)`:

* At all module boundaries
* On GPT payload receipt
* On API fallback triggers

Instruct user to paste `log_buffer.getvalue()` for tracebacks.
Set `DEBUG = False` before publishing.

---

### 5 · Testing & Quality

**pytest roadmap**

* `test_stock_fetch.py`:

  * Happy path for tickers & timeframes
  * Bad tickers, weekends
* `test_charts.py`:

  * Smoke tests for chart render
  * Sanity checks (e.g. 1 trace, axis present)
* `test_gpt_interface.py`:

  * Function schema matches
  * GPT inputs produce correct structured output

**Target:** ≥85% coverage
**CI Workflow:** GitHub Actions (lint → test)

---

### 6 · Documentation, Packaging & Artefacts

* ✅ **Docstrings only** (Google-style); no Sphinx
* ✅ `pyproject.toml` with semantic versioning (0.1.0 → public v1.0.0)
* ✅ `python -m build` and `twine` for optional wheel release

---

### 7 · Bias, Ethics & Scientific Rigour

* GPT does not offer financial advice; outputs are interpretive only.
* Data freshness depends on Yahoo API.
* Multiple chart types considered; fallbacks documented.
* Peer-reviewed sources unnecessary, but official API docs cited:

  * [Yahoo Finance via yfinance](https://pypi.org/project/yfinance/)
  * [OpenAI Function Calling Docs](https://platform.openai.com/docs/guides/function-calling)

---

### 8 · Deliverables & Timeline

| Milestone | Output                          | Owner   | ETA        |
| --------- | ------------------------------- | ------- | ---------- |
| 1         | Spec sheet v1                   | ChatGPT | 2025-06-09 |
| 2         | Prototype modules & basic tests | ChatGPT | 2025-06-12 |
| 3         | Production release candidate    | ChatGPT | 2025-06-14 |

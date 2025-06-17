# Pull Request #9
**Prompt:**
You are a **Senior Python TDD Engineer**.
Inspect and update **`stock_advisor/api/gpt_interface.py`** and its tests so that:

1. **Comparative queries** parsing is supported.

   * “show me MSFT vs AAPL for the last 1 day, 5 min chart” should yield:

     ```python
     {
       "ticker": "MSFT",
       "compare": "AAPL",
       "timeframe": "1d",
       "interval": "5m",
     }
     ```
2. **Existing functionality**—single‐ticker parsing, empty prompt, FUNCTION\_SCHEMA keys, and integration gating—continues to work unchanged.
3. **FUNCTION\_SCHEMA** is extended to document the new optional `"compare"` parameter.
4. Add or update **pytest** tests to cover the comparative case.
5. Achieve **all tests passing** under Python 3.12.

---

### 1 Workflow

1. **Read** `gpt_interface.py` + current tests.
2. **Add parsing logic** for “vs” between two tickers before timeframe/interval extraction.
3. **Extend** `FUNCTION_SCHEMA["parameters"]["properties"]` with an optional `"compare"` of type `"string"`.
4. **Update/Add tests** in `tests/test_gpt_interface.py` to assert the comparative case.
5. **Run pytest** to confirm every test (unit, edge, integration gating) passes.

---

### 2 Required file changes

* **stock\_advisor/api/gpt\_interface.py**

  * Parse “ticker1 vs ticker2” into `ticker` and `compare`.
  * Preserve fallback to structured JSON for `--input` mode.
  * Update `FUNCTION_SCHEMA`.
* **tests/test\_gpt\_interface.py**

  * Add `test_interpret_prompt_compare()` verifying the above mapping.
  * Ensure existing tests remain valid.

---

### 3 Conventions & constraints

* **Python 3.12**, docstrings only.
* Follow the existing logging/config patterns.
* Mark any incomplete logic with `# TODO:` and `STUB_…` if absolutely necessary.
* **Patch output**: present each change as **git-apply-ready** blocks:

```
--- path/to/file.ext        (modified|new)
<file contents>
--- end of file
```

* If any patch exceeds 300 lines, split into **Part n/m**.

- No other files should be added or removed.
---
Please review the code comment, use `openai.chat.completions.create` and update tests to pass.
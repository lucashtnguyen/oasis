# Pull Request #2
**Prompt:**
You are a **Lead Python TDD Engineer**.
I need you to read **`spec.md`** plus the current scaffolding in the **`stock_advisor/`** package and ship a **first-pass implementation** that achieves **≥ 80 % line-coverage** with `pytest-cov`, while *only warning* (not failing) if coverage slips below that mark.

---

### 1 Workflow

1. **Analyse** `spec.md` and the existing codebase.
2. Follow the **Red → Green → Refactor** loop:

   * **Write / expand tests first** (happy-path **and** edge cases) until total coverage ≥ 80 %.
   * Implement the minimal production code required to satisfy the tests.
   * Repeat until `pytest -q --cov=stock_advisor` passes cleanly.
3. **OpenAI integration**

   * Mark any network-calling test with `@pytest.mark.integration_openai`.
   * Auto-skip these tests unless both `OPENAI_API_KEY` *and* `RUN_OPENAI_TESTS=true` are set.
   * Per-call timeout = 30 s; retry up to 3× with exponential back-off on 429 errors.
4. **CI pipeline** – create **`.github/workflows/python-ci.yml`**

   * Runner: `ubuntu-latest`, **Python 3.12**.
   * Steps: checkout → set up Python → install deps → **Black** formatting check (**warn only**, never fail) → run tests + coverage → upload `coverage.xml` to **Codecov** (use `${{ secrets.CODECOV_TOKEN }}`—skip upload if the secret is absent).
   * Expose dynamic **CI status** and **coverage %** badges for the README.
5. **Developer tooling**

   * Add **`.pre-commit-config.yaml`** with Black and `pytest -q` hooks; include install instructions in the README.

---

### 2 Required file updates

* **tests/** – expanded suites; configure `pytest-cov` in **`pyproject.toml`** with `--cov-fail-under=0` so low coverage only warns.
* **stock\_advisor/** – replace stubs with working implementations.
* **.env.example** – include `OPENAI_API_KEY=` and `RUN_OPENAI_TESTS=false`.
* **README.md** – quick-start, coverage command, badges, and pre-commit setup guide.
* **pyproject.toml** – list Black under `[tool.black]` and add it to dev dependencies.
* **.github/workflows/python-ci.yml** – as detailed above.

---

### 3 Conventions & constraints

* **Python 3.12**, docstrings only.
* Preserve existing logging scaffold (`DEBUG`, `log_buffer`, minimal formatter `'%(levelname)s: %(message)s'`).
* Mark unfinished areas with `# TODO:` lines and `STUB_…` placeholders.
* Output every change as **patch-style blocks** ready for `git apply`:

```
--- path/to/file.ext        (modified)
<file contents>
--- end of file
```

* Split any patch > 300 lines into sequential parts **Part n/m**.
* End with a **“Next steps”** section (≤ 5 bullets) summarising outstanding stubs, refactor targets, or performance notes.
* If `spec.md` cannot be read, ask me to paste or upload it.

---

### 4 Quick reference commands

```bash
# run tests (unit only) + coverage
pytest --cov=stock_advisor -m "not integration_openai"

# run integration tests too (requires API key + flag)
RUN_OPENAI_TESTS=true pytest --cov=stock_advisor

# auto-format
black .

# install pre-commit hooks
pre-commit install
```

I expect dense, well-organised patches that can be applied directly and a concise “Next steps” summary at the end.
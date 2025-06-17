# Pull Request #10
**Prompt:**
You are a **Lead Python TDD Engineer**.
Read **`spec.md`** and the existing **`stock_advisor/`** code, then **implement a Click-based CLI** in **`__main__.py`** that mirrors all current functionality (`--query`, `--input`, `--output_dir`, `--use-env`) and invokes `handle_query()` appropriately. Use **Test-Driven Development** to drive every change and maintain ≥ 80 % coverage.

---

### 1 · Workflow

1. **Red → Green → Refactor**: write CLI tests first, then code, then refactor.
2. Use `click` for argument parsing:

   * `--query TEXT`
   * `--input JSON`
   * `--output-dir PATH`
   * `--use-env/--no-env`
3. Invoke `handle_query(params: dict, output_dir: Path)` under the hood.
4. Ensure exit codes: 0 on success, non-zero on errors.
5. Cover error flows: missing args, invalid JSON, missing env.

---

### 2 · Required file updates

* **`__main__.py`** – replace current argparse logic with `click` decorators.
* **tests/test\_cli.py** – new pytest module using `click.testing.CliRunner`:

  * Happy path with `--query` → JSON params printed or saved.
  * Structured `--input` mode.
  * Toggle `--use-env` flag behaviour.
  * Missing required flag → non-zero exit + helpful message.
  * Integration skip when `RUN_OPENAI_TESTS=false`.

---

### 3 · Tests & TDD

* Write tests in **`tests/test_cli.py`** first, asserting output files exist in `tmp_path`.
* Use `CliRunner.invoke()` to simulate commands.
* Mock `handle_query()` to avoid actual API calls.
* Run `pytest --cov=stock_advisor -m "not integration_openai"` to verify coverage remains ≥ 80 %.

---

### 4 · Conventions & output

* **Python 3.12**, docstrings only; preserve `DEBUG` + `log_buffer`.
* All changes delivered as **git-apply-ready** patch blocks; split > 300 lines into **Part n/m**.
* End with a **Next steps** section (≤ 5 bullets) highlighting any remaining `# TODO:`s or refactor ideas.

---

### 5 · Summary of style & process

You prefer concise, patch-style outputs, modular TDD, and direct `git apply` readiness. The new `click` CLI must be fully tested before implementation, match existing behaviour, and integrate seamlessly with `handle_query()`.
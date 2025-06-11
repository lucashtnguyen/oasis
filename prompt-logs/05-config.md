# Pull Request #5
**Prompt:**
You are a **Senior Python Infrastructure Engineer**.
**First, read `spec.md` in the repo root to confirm the original project scope and constraints, and ensure every change you make remains aligned with that spec.**
Extend the existing **ChatGPT Stock Advisor** repo (Python 3.12, CLI + module, no web UI) by **adding a secrets/config layer, environment-aware test gating, and minimal DX tooling**.
⚠️ **Do not remove or break current behaviour—only add or refactor, and stay strictly within the boundaries laid out in `spec.md`.**

---

### 1 · Dependencies & house-keeping

* Append **`python-dotenv`** and **`pydantic-settings`** to **requirements.txt** (or `[project.dependencies]` in *pyproject.toml* if that is canonical).
* Extend **.gitignore** with common secrets/venv patterns (e.g., `.env`, `.venv`, `__pycache__/`, IDE files).

---

### 2 · Secrets & config layer

Create **`config.py`** at repo root:

```python
"""Centralised settings for ChatGPT Stock Advisor."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load .env if present (noop in most CI environments)
load_dotenv(Path(__file__).with_name(".env"))

class Settings(BaseSettings):
    """Strongly-typed runtime configuration."""
    openai_api_key: str
    run_openai_tests: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

settings = Settings()          # import-safe singleton
```

* Raise `ValidationError` if `openai_api_key` is missing **and** `run_openai_tests` is `True`.
* Access via `from config import settings`.

---

### 3 · Inject secret into runtime code

Refactor every place that instantiates an `OpenAI` client:

```python
# BEFORE
client = OpenAI()

# AFTER
from config import settings
client = OpenAI(api_key=settings.openai_api_key)
```

---

### 4 · API integration-test gating

Add **`tests/test_openai_integration.py`**

```python
"""
Runs only when RUN_OPENAI_TESTS=true *and* OPENAI_API_KEY is set.
Execute with: pytest -q tests/test_openai_integration.py
"""
import pytest
from openai import OpenAI
from config import settings

_skip = not settings.run_openai_tests or not settings.openai_api_key
pytestmark = pytest.mark.skipif(_skip, reason="Integration tests disabled")

def test_chat_completion_smoke() -> None:
    """Minimal round-trip to verify credentials are valid."""
    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": "ping"}],
        max_tokens=1,
    )
    assert resp.choices[0].message.content.strip()
```

---

### 5 · CLI helper flag

In **`__main__.py`** add:

```python
@click.option(
    "--use-env/--no-env",
    default=True,
    help="Load variables from .env (default) or rely solely on OS env vars.",
)
def cli(query: str, output_dir: Path, use_env: bool = True) -> None:
    if not use_env:
        # Force reload with Settings that ignores .env
        os.environ.pop("PYTHON_DOTENV", None)
```

---

### 6 · CI secrets snippet (README)

Append to **README.md**:

```yaml
# ── Secrets in CI ───────────────────────
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  RUN_OPENAI_TESTS: "true"
```

---

### 7 · Refactor & quality guidelines

* Keep functions single-responsibility; avoid circular imports.
* Preserve existing logging scaffold (`DEBUG`, `log_buffer`).
* All new code **PEP 8** + inline docstrings.
* Mark future work with `# TODO:` and `STUB_…` placeholders.
* Maintain ≥ 80 % pytest-cov coverage: integration test is **skipped by default**, so unit numbers must still hit the bar.

---

### 8 · Deliverables

1. **requirements.txt**, **pyproject.toml**, & **.gitignore** updates 
2. **config.py** module
3. Runtime refactors to import `settings.openai_api_key`
4. **tests/test\_openai\_integration.py** (auto-skip logic)
5. Updated **`__main__.py`** CLI flag
6. README secrets-in-CI snippet

---

### 9 · Output instructions

* Return all changes as **patch-style blocks** ready for `git apply`:

```
--- path/to/file.ext        (new|modified)
<file contents>
--- end of file
```
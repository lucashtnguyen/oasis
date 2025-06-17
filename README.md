# Stock Advisor

You’re right — here’s the **balanced** version: technically sharp, purpose-driven, and with just the right amount of fun baked in.

---

**Project Preamble — ChatGPT Stock Advisor**

*ChatGPT Stock Advisor* wasn’t built to chart stocks—it was built to **discover what modern Python development looks like when you put Codex in the passenger seat and keep both hands on the wheel**. This project showcases a clean, test-driven workflow using **Python 3.12**, **Plotly**, **click**, **pytest**, and **OpenAI’s function-calling API**, all wrapped in a modular CLI tool that turns plain English prompts like “Show me the 5-minute chart for MSFT today” into interactive charts and GPT-powered summaries. The goal? Not to reinvent the wheel—but to **explore rapidly growing  tools that matter**: Codex-assisted scaffolding, TDD, reproducible outputs, and AI-enhanced logic that plays nice with version control. Every part of the system—from data fetching to visualization—is built for clarity, modularity, and ease of extension driven by strong Codex prompts as much as possible. And in case you're wondering how much of this was vibes vs. design, the full trail of Codex prompts lives in `/prompt-logs` and are numbered based on PR. I approched this with 80:20 in mind, only touching the code for quick fixes. I designed these prompts as though Codex is a junior level engineer, giving clear instruction to maintain clarity and mission in its work product. 

This V0.1.0 release is very much a MVP, but it's amazing how quickly I got here using what I'll call *vibes++* coding.

[![CI](https://github.com/lucashtnguyen/oasis/actions/workflows/python-ci.yml/badge.svg)](https://github.com/lucashtnguyen/oasis/actions/workflows/python-ci.yml)
[![Coverage](https://codecov.io/gh/lucashtnguyen/oasis/branch/main/graph/badge.svg)](https://codecov.io/gh/OWNER/REPO)

## Quick-start for contributors

1. **Create a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. **Install dependencies**

```bash
pip install -e .[dev]
```

3. **Run tests**

```bash
pytest --cov=stock_advisor -m "not integration_openai"
```

4. **Set up pre-commit hooks**

```bash
pre-commit install
```

5. **Run example**

```bash
python -m stock_advisor --query "Show me AAPL for last week" --output_dir output
```

```yaml
# ── Secrets in CI ───────────────────────
env:
  OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
  RUN_OPENAI_TESTS: "true"
```

```bash
stock_advisor --query "show me MSFT for the last day, 5 minute chart"
```

![MSFT](https://github.com/lucashtnguyen/oasis/images/show-me-msft.png "MSFT")


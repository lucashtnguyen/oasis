# Stock Advisor

LLM-assisted tool for fetching and visualizing stock data.

![CI](https://github.com/OWNER/REPO/actions/workflows/python-ci.yml/badge.svg)
![Coverage](https://codecov.io/gh/OWNER/REPO/branch/main/graph/badge.svg)

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
python -m stock_advisor --help
```


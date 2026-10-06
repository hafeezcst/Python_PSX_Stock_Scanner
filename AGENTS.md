# AGENTS.md

## Cursor Cloud specific instructions

This repo is a **Python 3.12** collection of command-line scripts for stock/crypto
technical analysis (Pakistan Stock Exchange "PSX", Qatar "QSE", crypto, Nifty). It
is **not** a web app or monorepo: there is no server, no build step required to run,
and modules are coupled only through the shared filesystem (`.xlsx`, `.csv`, SQLite
`.db` files). Data comes from the live **TradingView** API via the `tradingview_ta`
package, so all scanning requires **internet access**.

### Dependencies
- The dependency-refresh update script installs the core packages. Runtime deps are
  also listed in `requirements.txt`. `pip` installs into the user site
  (`~/.local`), no venv is used.
- `MetaTrader5` (used only by `MT5 Connection/*`) is Windows-only and intentionally
  NOT installed on Linux; that module is out of scope here.

### Running things (all commands run from the repo root)
- Scripts use paths relative to the CWD (e.g. `PSXSymbols.xlsx`, `config.ini`,
  `analysis_log.txt`), so always run from `/workspace`.
- To import repo modules from a script outside the repo, set `PYTHONPATH=/workspace`.
- Main scanner entrypoint: `python3 main_PSX.py`. NOTE: it is **not headless** — it
  scans the full KMI100 + QSE universes and, at the end, **sends real emails**
  (credentials committed in `config.ini`) and posts to a **real Telegram group**
  (token hardcoded in `telegram_message.py`). Avoid running it as-is during dev
  unless you intend to send those notifications. To exercise the core pipeline
  (symbol list -> `analyze_symbol` -> pandas -> SQLite + Excel) without the
  email/Telegram side effects, call `analysis_functions.analyze_symbol(...)` and the
  pandas/openpyxl write logic directly.
- Signal scripts (`PSX_Signal_RSI30.py`, `QSE_SIGNAL*.py`, `Crypto_Signal*.py`) run
  **infinite loops** with `time.sleep` waits and also push to Telegram/email — they
  do not terminate on their own.

### Tests
- `python3 -m unittest test_main_PSX.py` (or `python3 -m pytest`). Tests hit the live
  TradingView API (no mocking), so they need network.
- `test_main_PSX.py` currently **fails as written**: it requests symbol `AAPL` on the
  Pakistan `PSX` exchange, which does not exist there, so `analyze_symbol` correctly
  returns `None` and the assertion fails. This is a pre-existing test bug, not an
  environment problem.

### Lint / build
- No linter or lint config is present (no ruff/flake8/black/pylint).
- No build is needed to run. PyInstaller `.spec` files exist for packaging Windows
  executables, and `.github/workflows/python-publish.yml` builds a PyPI package, but
  neither is required for local development.

# Function Reference — DataBot Analytics (English)

This document summarizes the core functions by module. It may not be fully exhaustive; refer to source files for the latest code.

## bot.py — Bot logic
- class DataAnalyticsBot
  - __init__(self)
    - Loads token from environment, builds the python-telegram-bot Application, calls setup_handlers.
  - setup_handlers(self)
    - Registers handlers:
      - /start → start
      - /help → help_command
      - /analyze → analyze (if present in current version)
      - /visualize → visualize (if present)
      - /charts → create_charts (if present)
      - Documents → handle_document
      - Text → handle_text
  - start(self, update, context) [async]
    - Welcome message and usage instructions.
  - help_command(self, update, context) [async]
    - Detailed help about commands, supported files, and workflow.
  - handle_document(self, update, context) [async]
    - Accepts CSV/XLS/XLSX, validates extension, downloads into memory, prepares for analysis.
  - handle_text(self, update, context) [async]
    - Basic text interactions (greeting/help/hints for charts).
  - quick_analysis(self, df, filename)
    - Quick stats: rows/columns, memory, missing/duplicates, completeness; returns a ready-to-send summary.
  - detailed_analysis(self, df, filename)
    - Detailed numeric stats (and correlations if multiple numeric columns).

## bot_runner.py — Bot runner
- Runs the bot in long polling via `application.run_polling()`.

## main.py — Combined run (local)
- run_bot() — runs bot.py in a subprocess with colored logs.
- run_streamlit() — runs Streamlit on app.py.
- __main__ block — creates two threads (bot + Streamlit).

## app.py — Streamlit app
- main() — UI entry, configuration, navigation, and display areas.
- _db_path() → str — returns SQLite path (uploaded_data.db) for uploaded files.
- _run_sql(query: str) → pd.DataFrame — executes SQL on uploaded_data.db and returns DataFrame.
- _show_query_insights(df: pd.DataFrame) → None — compact stats + quick bar chart if small result.
- _sqlite_db_path() → str — SQLite DB path.
- _normalize_table_name(raw: str, fallback_idx: int = 1) → str — safe table name from CSV file name.
- _sqlite_run_sql(query: str) → pd.DataFrame — runs query on uploaded_data.db.

## config.py — Configuration
- TELEGRAM_TOKEN — read from os.getenv.
- PAGE_TITLE, PAGE_ICON, LAYOUT — Streamlit UI settings.
- COLORS — UI color palette.

## streamlit_app.py — Streamlit wrapper
- Loads mobile notices and executes app.py.

## mobile_notice.py — Mobile notices
- Displays mobile-related messages inside Streamlit.
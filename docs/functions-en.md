# 📚 Function Reference — DataBot Analytics (English)

This document summarizes core functions by module. It may not be exhaustive; see sources for the latest code. ✨

## 🤖 bot.py — Bot logic
- class DataAnalyticsBot
  - __init__(self) — loads token, builds Application, calls setup_handlers.
  - setup_handlers(self) — registers handlers:
    • /start → start  
    • /help → help_command  
    • /analyze → analyze (if present)  
    • /visualize → visualize (if present)  
    • /charts → create_charts (if present)  
    • Documents → handle_document  
    • Text → handle_text
  - start(...) [async] — welcome and usage. 
  - help_command(...) [async] — detailed help. 
  - handle_document(...) [async] — CSV/XLS/XLSX ingestion and prep. 
  - handle_text(...) [async] — basic text interactions. 
  - quick_analysis(df, filename) — quick stats summary. 📊
  - detailed_analysis(df, filename) — detailed numeric stats and correlations. 📈

## ▶️ bot_runner.py — Bot runner
- Runs long polling via `application.run_polling()`. ⏱️

## 🧩 main.py — Combined run (local)
- run_bot() — runs bot.py in a subprocess with colored logs. 🎨
- run_streamlit() — runs Streamlit on app.py. 🖥️
- __main__ — spawns two threads (bot + Streamlit). 🧵

## 🖥️ app.py — Streamlit app
- main() — UI entry, configuration, navigation. 🧭
- _db_path() → str — local DB path (uploaded_data.db). 💾
- _run_sql(query: str) → pd.DataFrame — executes SQL on uploaded_data.db. 🧮
- _show_query_insights(df) → None — compact stats and quick bar chart. 📊
- _sqlite_db_path() → str — SQLite DB path. 🗄️
- _normalize_table_name(raw, fallback_idx=1) → str — safe table name from CSV. 🧹
- _sqlite_run_sql(query) → pd.DataFrame — runs a query on uploaded_data.db. 🔎

## ⚙️ config.py — Configuration
- TELEGRAM_TOKEN — read from os.getenv. 🔑
- PAGE_TITLE, PAGE_ICON, LAYOUT — Streamlit UI. 🎛️
- COLORS — UI color palette. 🎨

## 🧩 streamlit_app.py — Streamlit wrapper
- Loads mobile notices and executes app.py. 📱

## 📱 mobile_notice.py — Mobile notices
- Mobile-friendly messages inside Streamlit. 📢
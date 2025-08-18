# DataBot Analytics — הבוט של Artisa111

זה הבוט שלי (Artisa111) לניתוח נתונים בטלגרם, יחד עם אפליקציית Streamlit להצגת דשבורדים. הפרויקט מותאם לפריסה קלה ב‑Railway, עם תצורה פשוטה, לוגים ברורים ותיעוד דו‑לשוני.

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Artisa111/databot-analytics&envs=TELEGRAM_TOKEN&name=DataBot%20Analytics&description=Telegram%20data%20bot%20%2B%20Streamlit)

— הערה: לאחר הפריסה, הגדירו את משתנה הסביבה TELEGRAM_TOKEN. 

## מה יש כאן
- בוט טלגרם ב‑Python (Long Polling)
- אפליקציית Streamlit להצגת ניתוחים וגרפים
- פריסה פשוטה ל‑Railway עם כפתור "Deploy"
- תצורה באמצעות משתני סביבה בלבד (ללא טוקנים בקוד)

## התקנה מקומית
1) דרישות: Python 3.11+, pip

2) התקנה:
```bash
git clone https://github.com/Artisa111/databot-analytics.git
cd databot-analytics
pip install -r requirements.txt
```

3) משתני סביבה (מקומי, אופציונלי דרך .env):
```env
TELEGRAM_TOKEN=הטוקן_שלכם_מבוטפאדר
```

4) הרצה מקומית:
- בוט בלבד: `python bot_runner.py`
- Streamlit בלבד: `streamlit run app.py`
- הרצה משולבת לדמו: 
```bash
sh -c "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & python bot_runner.py"
```

## פריסה ל‑Railway
- לחצו על הכפתור למעלה או חברו את הריפו אל Railway.
- הגדירו Variable בשם TELEGRAM_TOKEN עם הטוקן המדויק של הבוט.
- פקודת Start מומלצת:
```bash
sh -c "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 & python bot_runner.py"
```

## אבטחה
- לעולם אל תתחייבו (commit) טוקנים לקוד.
- השתמשו במשתני סביבה לניהול סודות.

## מבנה הפרויקט (תקציר)
```
.
├── app.py                # אפליקציית Streamlit
├── bot.py                # לוגיקת הבוט וה‑handlers
├── bot_runner.py         # מפעיל הבוט (Polling)
├── main.py               # הרצה משולבת מקומית (בוט + Streamlit)
├── config.py             # קונפיגורציה כללית
├── streamlit_app.py      # מעטפת הרצה ל‑Streamlit
├── mobile_notice.py      # הודעות התאמה למובייל
└── README.md
```

## קרדיט
- נכתב ומנוהל ע"י Artisa111 — זה הבוט שלי.

—

# DataBot Analytics — Artisa111's Bot

This is my bot (Artisa111) for Telegram data analysis, paired with a Streamlit app for visual dashboards. The project is designed for easy deployment on Railway with simple configuration and clear logs. Documentation is bilingual (Hebrew and English).

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://github.com/Artisa111/databot-analytics&envs=TELEGRAM_TOKEN&name=DataBot%20Analytics&description=Telegram%20data%20bot%20%2B%20Streamlit)

## Features
- Telegram bot in Python (long polling)
- Streamlit app for charts and analytics
- One‑click Railway deployment
- Environment‑only secrets (no tokens in code)

## Local Setup
1) Requirements: Python 3.11+, pip

2) Install:
```bash
git clone https://github.com/Artisa111/databot-analytics.git
cd databot-analytics
pip install -r requirements.txt
```

3) Environment variables (local, via .env or system):
```env
TELEGRAM_TOKEN=your_botfather_token_here
```

4) Run locally:
- Bot only: `python bot_runner.py`
- Streamlit only: `streamlit run app.py`
- Combined (demo):
```bash
sh -c "streamlit run app.py --server.port=8501 --server.address=0.0.0.0 & python bot_runner.py"
```

## Deploy on Railway
- Click the button above or connect the repo in Railway.
- Set TELEGRAM_TOKEN in Variables.
- Recommended Start Command:
```bash
sh -c "streamlit run app.py --server.port=${PORT:-8501} --server.address=0.0.0.0 & python bot_runner.py"
```

## Security
- Never commit tokens to the repo.
- Use environment variables for secrets.

## Project Structure (short)
```
.
├── app.py
├── bot.py
├── bot_runner.py
├── main.py
├── config.py
├── streamlit_app.py
├── mobile_notice.py
└── README.md
```

## Credits
- Built and maintained by Artisa111 — this is my bot.

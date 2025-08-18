<div dir="rtl" lang="he" align="right">

# 📚 תיעוד פונקציות — DataBot Analytics (עברית)

המסמך מסכם את הפונקציות העיקריות לפי מודולים (יתכנו שינויים בין גרסאות). ראו גם את קבצי המקור. ✨

## 🤖 bot.py — לוגיקת הבוט
- class DataAnalyticsBot
  - __init__(self) — טוען טוקן, יוצר Application וקורא ל‑setup_handlers.
  - setup_handlers(self) — רישום handlers לפקודות/הודעות:  
    • /start → start  
    • /help → help_command  
    • /analyze → analyze (אם קיימת)  
    • /visualize → visualize (אם קיימת)  
    • /charts → create_charts (אם קיימת)  
    • מסמכים → handle_document  
    • טקסט → handle_text
  - start(...) [async] — הודעת פתיחה והוראות שימוש.
  - help_command(...) [async] — עזרה מפורטת על פקודות וקבצים נתמכים.
  - handle_document(...) [async] — קבלת CSV/XLS/XLSX, בדיקה, הורדה לזיכרון והכנה לניתוח.
  - handle_text(...) [async] — אינטראקציות טקסטואליות (ברכות/עזרה/רמזים לגרפים).
  - quick_analysis(df, filename) — סטטיסטיקות מהירות: שורות/עמודות/זיכרון/חסרים/כפולים/שלמות. 📊
  - detailed_analysis(df, filename) — סטטיסטיקה מפורטת ו‑correlation אם יש מספיק עמודות. 📈

## ▶️ bot_runner.py — מפעיל הבוט
- מריץ Long Polling דרך `application.run_polling()`. ⏱️

## 🧩 main.py — הרצה משולבת (מקומי)
- run_bot() — מריץ את bot.py בתהליך משנה עם לוג צבעוני. 🎨
- run_streamlit() — מריץ Streamlit על app.py. 🖥️
- __main__ — יוצר שני threads (בוט + Streamlit). 🧵

## 🖥️ app.py — אפליקציית Streamlit
- main() — כניסת UI, קונפיגורציה וניווט. 🧭
- _db_path() → str — נתיב מסד נתונים מקומי (uploaded_data.db). 💾
- _run_sql(query: str) → pd.DataFrame — הרצת SQL על uploaded_data.db. 🧮
- _show_query_insights(df) → None — סטטיסטיקות קצרות ותרשים בר מהיר. 📊
- _sqlite_db_path() → str — נתיב DB ל‑SQLite. 🗄️
- _normalize_table_name(raw, fallback_idx=1) → str — נרמול שם טבלה בטוח מ‑CSV. 🧹
- _sqlite_run_sql(query) → pd.DataFrame — הרצת שאילתה על uploaded_data.db. 🔎

## ⚙️ config.py — קונפיגורציה
- TELEGRAM_TOKEN — קריאה מ‑os.getenv. 🔑
- PAGE_TITLE, PAGE_ICON, LAYOUT — עיצוב ל‑Streamlit. 🎛️
- COLORS — צבעי UI. 🎨

## 🧩 streamlit_app.py — מעטפת ל‑Streamlit
- טוען הודעות מובייל ומריץ את app.py. 📱

## 📱 mobile_notice.py — הודעות מובייל
- הודעות והתאמות למשתמשי מובייל בתוך Streamlit. 📢

</div>
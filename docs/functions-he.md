# תיעוד פונקציות — DataBot Analytics (עברית)

המסמך מסכם את הפונקציות העיקריות לפי מודולים. ייתכן שהרשימה אינה מלאה לחלוטין (הקוד מתעדכן). ראו גם את קבצי המקור.

## bot.py — לוגיקת הבוט
- class DataAnalyticsBot
  - __init__(self)
    - טוען את הטוקן מהסביבה, בונה Application של python-telegram-bot, וקורא ל‑setup_handlers.
  - setup_handlers(self)
    - רושם את ה‑handlers לפקודות והודעות:
      - /start → start
      - /help → help_command
      - /analyze → analyze (אם קיימת בגרסה הנוכחית)
      - /visualize → visualize (אם קיימת)
      - /charts → create_charts (אם קיימת)
      - קבצים → handle_document
      - טקסט → handle_text
  - start(self, update, context) [async]
    - הודעת פתיחה עם הוראות שימוש.
  - help_command(self, update, context) [async]
    - עזרה מפורטת על פקודות, קבצים נתמכים וזרימת עבודה.
  - handle_document(self, update, context) [async]
    - קבלת קבצים (CSV/XLS/XLSX), בדיקת סיומת, הורדה לזיכרון והכנה לניתוח.
  - handle_text(self, update, context) [async]
    - אינטראקציות טקסטואליות (ברכות, עזרה, הכוונה ליצירת גרפים).
  - quick_analysis(self, df, filename)
    - ניתוח מהיר: שורות/עמודות, זיכרון, חסרים/כפולים, אחוז שלמות, סיכום מוכן לשליחה.
  - detailed_analysis(self, df, filename)
    - ניתוח מפורט לעמודות נומריות (כולל סטטיסטיקות וקורלציות אם יש יותר מעמודה אחת).

## bot_runner.py — מפעיל הבוט
- מריץ את הבוט ב‑Long Polling דרך `application.run_polling()`.

## main.py — הרצה משולבת (מקומי)
- run_bot() — מריץ את bot.py בתהליך משנה עם לוג צבעוני.
- run_streamlit() — מריץ Streamlit על app.py.
- בלוק __main__ — יוצר שני threads, אחד לבוט ואחד ל‑Streamlit.

## app.py — אפליקציית Streamlit
- main() — כניסת UI, קונפיגורציה, ניווט ואזורי תצוגה.
- _db_path() → str — מחזיר מיקום SQLite המקומי (uploaded_data.db) לקבצים שהועלו.
- _run_sql(query: str) → pd.DataFrame — מריץ SQL על uploaded_data.db ומחזיר DataFrame.
- _show_query_insights(df: pd.DataFrame) → None — מציג סטטיסטיקות קצרות וגרף בר בהינתן תוצאה קטנה.
- _sqlite_db_path() → str — נתיב DB ל‑SQLite.
- _normalize_table_name(raw: str, fallback_idx: int = 1) → str — נרמול שם טבלה בטוח מ‑CSV.
- _sqlite_run_sql(query: str) → pd.DataFrame — מריץ שאילתה על uploaded_data.db.

## config.py — קונפיגורציה
- TELEGRAM_TOKEN — קריאה מ‑os.getenv.
- PAGE_TITLE, PAGE_ICON, LAYOUT — הגדרות עיצוב.
- COLORS — מילון צבעים לממשק.

## streamlit_app.py — מעטפת ל‑Streamlit
- טוען הודעות מובייל ומריץ את app.py.

## mobile_notice.py — הודעות מובייל
- מציג אזהרות והתאמות למובייל בתוך Streamlit.
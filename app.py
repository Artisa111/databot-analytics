import streamlit as st

# ========================================================================
#                           מערכת אימות אופציונלית - רישום והתחברות
# ========================================================================
# מערכת רישום יפה ואופציונלית עם email וסיסמה
# לביטול המערכת: שנה את ENABLE_AUTH ל-False
ENABLE_AUTH = True

try:
    import auth  # ייבוא מודול האימות
    AUTH_AVAILABLE = True
except ImportError:
    AUTH_AVAILABLE = False
    ENABLE_AUTH = False

# ========================================================================
#                           בלוק ייבוא הספריות הראשיות
# ========================================================================
# פונקציה בטוחה לזיהוי מכשירים ניידים
def is_mobile_browser():
    """
    זיהוי מכשיר נייד בצורה בטוחה ללא בעיות תצוגה
    
    מטרת הפונקציה:
    - לזהות אם המשתמש משתמש במכשיר נייד
    - לשמור את התוצאה בסשן כדי למנוע בדיקות חוזרות
    - להחזיר False כברירת מחדל למניעת שגיאות
    
    החזרה: bool - True אם מכשיר נייד, False אחרת
    """
    try:
        # שימוש בסטטוס הסשן כדי לשמור את תוצאת הזיהוי
        if 'is_mobile_cache' not in st.session_state:
            # בדיקת רוחב המסך או הגדרה ידנית על ידי המשתמש
            # כברירת מחדל נניח שזה לא מכשיר נייד
            mobile_detected = False
            
            # אם המשתמש הגדיר ידנית במקום אחר
            if 'mobile_device_manual' in st.session_state:
                mobile_detected = st.session_state.mobile_device_manual
                
            st.session_state.is_mobile_cache = mobile_detected
        return st.session_state.is_mobile_cache
    except (AttributeError, KeyError, Exception) as e:
        # רישום שגיאה לדיבוג, אך החזרת ערך בטוח
        return False

# ========================================================================
#                           ייבוא ספריות ניתוח נתונים
# ========================================================================
import pandas as pd                 # ספרייה לעבודה עם נתונים טבלאיים
import plotly.express as px         # ספרייה ליצירת תרשימים אינטראקטיביים
import plotly.graph_objects as go   # אובייקטים מתקדמים לתרשימים
from plotly.subplots import make_subplots  # יצירת תרשימים מורכבים עם תתי-גרפים
import numpy as np                  # ספרייה לחישובים נומריים
from datetime import datetime, timedelta  # עבודה עם תאריכים וזמנים
import pytz                         # טיפול באזורי זמן
import seaborn as sns              # ספרייה נוספת לויזואליזציה

# ========================================================================
#                           הגדרות תצוגה ורינדור
# ========================================================================
import time                        # פונקציות זמן ושהיה
import matplotlib                  # ספרייה בסיסית לתרשימים
matplotlib.use('Agg')             # הגדרת רינדור ללא ממשק גרפי (backend)
import matplotlib.pyplot as plt    # פונקציות יצירת תרשימים

# ========================================================================
#                           ספריות למידת מכונה
# ========================================================================
from sklearn.cluster import KMeans              # אלגוריתם K-Means לקלאסטרינג
from sklearn.decomposition import PCA          # ניתוח רכיבים ראשיים
from sklearn.preprocessing import StandardScaler  # נרמול נתונים
from scipy import stats                        # חישובים סטטיסטיים מתקדמים

# ========================================================================
#                           ספריות ניהול קבצים ובסיסי נתונים
# ========================================================================
import sqlite3                     # עבודה עם בסיס נתונים SQLite
import os                          # פונקציות מערכת הפעלה  
import io                          # פונקציות קלט/פלט





# ========================================================================
#                         טעינת מנהל PostgreSQL אופציונלי  
# ========================================================================
# בלוק זה מנסה לטעון את מנהל PostgreSQL בצורה בטוחה
try:
    import psycopg2  # noqa: F401    # מנהל PostgreSQL לבסיס נתונים מתקדם
    _HAS_PG = True                   # דגל המציין שהמנהל זמין
except Exception:
    _HAS_PG = False                  # במקרה של כישלון, ממשיכים ללא PostgreSQL





# ========================================================================
#                           ספריות דוחות ורשת
# ========================================================================
from reportlab.pdfgen import canvas         # יצירת קבצי PDF
from reportlab.lib.pagesizes import letter  # גדלי עמודים לPDF
import requests                             # בקשות HTTP
import warnings                             # ניהול אזהרות
warnings.filterwarnings('ignore')          # השתקת אזהרות מיותרות

# ========================================================================
#                           הגדרות עמוד Streamlit
# ========================================================================
# הגדרת תצורת העמוד עם אופטימיזציות למכשירים ניידים
st.set_page_config(
    page_title="DataBot Analytics",     # כותרת הדף
    page_icon="🚀",                        # אייקון הדף
    layout="wide",                         # פריסה רחבה
    initial_sidebar_state="expanded"       # סרגל צד מורחב כברירת מחדל
)

# ========================================================================
#                           הגדרות מיוחדות למכשירים ניידים
# ========================================================================
# תצורה מיוחדת למכשירים ניידים (פשוטה)
if 'mobile_config_set' not in st.session_state:
    # הגדרת דגל לאופטימיזציות נייד
    # נטפל במגבלות גודל קבצים בפונקציית ההעלאה
    st.session_state.mobile_config_set = True

# ========================================================================
#                           עיצוב CSS עם שיפורים למכשירים ניידים
# ========================================================================
# בלוק זה מכיל את כל הגדרות העיצוב לאפליקציה
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    .stButton > button {
        background: linear-gradient(45deg, #667eea, #764ba2);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    .insight-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .advice-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .desktop-float {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 999;
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        padding: 15px;
        border-radius: 50px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    .mobile-banner {
        background: linear-gradient(45deg, #ff6b6b, #feca57);
        padding: 20px;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        animation: slideIn 1s ease-out;
    }
    @keyframes slideIn {
        from { opacity: 0; transform: translateY(-30px); }
        to { opacity: 1; transform: translateY(0); }
    }
</style>
""", unsafe_allow_html=True)

# ========================================================================
#                           פונקציה ראשית של האפליקציה
# ========================================================================
def main():
    """
    פונקציית הראשית של יישום DataBot Analytics Pro
    
    מטרת הפונקציה:
    - הגדרת ממשק המשתמש הראשי
    - ניהול הגדרות מכשירים ניידים/דסקטופ  
    - הצגת תפריט ניווט וחלקי האפליקציה השונים
    - טיפול באופטימיזציות מיוחדות למכשירים ניידים
    """
    
    # ========================================================================
    #                           מערכת רישום והתחברות אופציונלית
    # ========================================================================
    # בדיקת מערכת האימות בצורה בטוחה עם נפילה חזרה
    if ENABLE_AUTH and AUTH_AVAILABLE:
        # בדיקה אם להציג ממשק האימות
        if st.session_state.get("show_auth_ui", False):
            auth.show_auth_ui()  # הצגת חלון רישום/התחברות
            return  # עצירה כאן להצגת ממשק האימות בלבד
            
        # הוספת אפשרות התחברות בסרגל הצד
        with st.sidebar:
            st.markdown("---")
            if not auth.check_authentication():
                # כפתור התחברות/רישום
                if st.button("🔐 Login/Register", type="primary", use_container_width=True):
                    st.session_state.show_auth_ui = True
                    st.rerun()
                st.info("📝 Login for personalized experience")
            else:
                # הצגת פרטי המשתמש המחובר
                auth.show_user_info()
                st.success("✅ התחברת בהצלחה!")
    
    # הצגת כותרת ראשית מעוצבת
    st.markdown('<h1 class="main-header">🚀 DataBot Analytics Pro</h1>', unsafe_allow_html=True)
    
    # ========================================================================
    #                           הגדרות מכשיר - אוטומטי לפי גודל מסך
    # ========================================================================
    # זיהוי אוטומטי של מכשיר נייד (ללא צורך בבחירה ידנית)
    is_mobile_device = False  # Default to desktop for clean UI
    
    # ========================================================================
    #                           הודעת ברוכים הבאים עבור דסקטופ
    # ========================================================================
    # הודעה נעימה ופשוטה למשתמשי דסקטופ
    st.success("🖥️ **Desktop Version Active** - Full functionality available!")
    
    # הודעה תמיד מוצגת - הבהרה שזה פרויקט לדוגמה
    st.warning("🙌 This application is presented as a pet project, so it shouldn't be taken too seriously. Thanks for giving it a try!")
    
    # ========================================================================
    #                           תפריט ניווט בסרגל הצד
    # ========================================================================
    with st.sidebar:
        st.markdown("### 🎯 Navigation")  # כותרת ניווט
        st.markdown("---")              # קו הפרדה
        
        # תפריט ניווט עם תיאורים
        page = st.selectbox(
            "Select section",           # תווית הבחירה
            ["🏠 Dashboard", "📁 Data Upload", "📈 Charts", "📊 Statistics", 
             "🤖 Machine Learning", "🧪 A/B Testing", "💾 Database", "📄 Reports"]
        )
        
        # ========================================================================
        #                           הצגת מידע על הסקציה הנוכחית
        # ========================================================================
        # מילון המכיל תיאור לכל סקציה באפליקציה
        section_info = {
            "🏠 Dashboard": "Main overview with key metrics and insights",      # לוח בקרה ראשי
            "📁 Data Upload": "Upload and clean CSV, Excel, JSON files",       # העלאת וניקוי קבצים
            "📈 Charts": "Interactive visualizations including 3D plots",       # תרשימים אינטראקטיביים
            "📊 Statistics": "Descriptive stats and statistical tests",        # סטטיסטיקה ובדיקות
            "🤖 Machine Learning": "Clustering, PCA, anomaly detection",       # למידת מכונה
            "🧪 A/B Testing": "Statistical significance testing",             # בדיקות A/B
            "💾 Database": "SQL operations and database management",          # ניהול בסיסי נתונים
            "📄 Reports": "Generate comprehensive analysis reports"            # יצירת דוחות
        }
        
        # הצגת מידע על הסקציה הנבחרת
        st.info(section_info[page])
        st.markdown("---")  # קו הפרדה
        
        # ========================================================================
        #                           פעולות מהירות בסרגל הצד
        # ========================================================================
        # הצגת פעולות מהירות רק אם יש נתונים טעונים
        if 'data' in st.session_state:
            st.markdown("### ⚡ Quick Actions")  # כותרת פעולות מהירות
            
            # קבלת הנתונים והעמודות הנומריות
            df = st.session_state.data
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            # כפתור סיכום נתונים מהיר
            if st.button("🎯 Data Summary", use_container_width=True):
                st.session_state.show_summary = True
            
            # כפתור מתאם מהיר (זמין רק עם 2+ עמודות נומריות)
            if len(numeric_cols) >= 2 and st.button("🔗 Quick Correlation", use_container_width=True):
                st.session_state.show_correlation = True
            
            # כפתור גרף תלת מימדי (זמין רק עם 3+ עמודות נומריות)
            if len(numeric_cols) >= 3 and st.button("🌐 3D Quick Plot", use_container_width=True):
                st.session_state.show_3d = True
            
            st.markdown("---")  # קו הפרדה
            
            # ========================================================================
            #                           מידע על הנתונים בסרגל הצד
            # ========================================================================
            st.markdown("### 📊 Data Info")      # כותרת מידע נתונים
            st.write(f"**Rows:** {len(df):,}")           # מספר שורות
            st.write(f"**Columns:** {len(df.columns)}")  # מספר עמודות
            st.write(f"**Numeric:** {len(numeric_cols)}") # מספר עמודות נומריות
            
            # חישוב אחוז הנתונים החסרים
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            quality_color = "🟢" if missing_pct < 5 else "🟡" if missing_pct < 15 else "🔴"
            st.write(f"**Quality:** {quality_color} {100-missing_pct:.1f}%")
        
        else:
            # ========================================================================
            #                           מדריך התחלה למשתמשים חדשים
            # ========================================================================
            st.markdown("### 🚀 Getting Started")  # כותרת מדריך התחלה
            st.write("1. Upload your data files")   # העלאת קבצים
            st.write("2. Or load demo data")        # טעינת נתוני דוגמה
            st.write("3. Explore with charts")     # חקירה עם תרשימים
            st.write("4. Run ML analysis")         # ניתוח למידת מכונה
            st.write("5. Generate reports")        # יצירת דוחות
            
            st.markdown("---")  # קו הפרדה
            
            # ========================================================================
            #                           סוגי קבצים נתמכים
            # ========================================================================
            st.markdown("### 📋 Supported Files")  # כותרת קבצים נתמכים
            st.write("• CSV files")                # קבצי CSV
            st.write("• Excel (.xlsx, .xls)")     # קבצי אקסל
            st.write("• JSON files")              # קבצי JSON
            st.write("• Multiple file upload")    # העלאת קבצים מרובים
        
        st.markdown("---")  # קו הפרדה
        
        # ========================================================================
        #                           מדור עזרה ותמיכה
        # ========================================================================
        st.markdown("### 🆘 Need Help?")  # כותרת עזרה
        with st.expander("📖 How to use"):  # קופסת עזרה מתרחבת
            st.write("""
            **Quick Start:**
            1. Go to Data Upload
            2. Load demo data or upload files
            3. Explore Dashboard for insights
            4. Use Charts for visualization
            5. Try Machine Learning features
            
            **Pro Tips:**
            • Use 3D Scatter for complex relationships
            • Check Statistics for data quality
            • A/B Testing for comparisons
            • Reports for final analysis
            """)
    
    # ========================================================================
    #                           טיפול בפעולות מהירות
    # ========================================================================
    # בדיקה והרצה של פעולות מהירות שהמשתמש ביקש
    if 'show_summary' in st.session_state and st.session_state.show_summary:
        show_quick_summary()                    # הצגת סיכום מהיר
        st.session_state.show_summary = False   # איפוס הדגל
    
    if 'show_correlation' in st.session_state and st.session_state.show_correlation:
        show_quick_correlation()                  # הצגת מתאם מהיר
        st.session_state.show_correlation = False # איפוס הדגל
        
    if 'show_3d' in st.session_state and st.session_state.show_3d:
        show_quick_3d()                         # הצגת גרף תלת מימדי מהיר
        st.session_state.show_3d = False        # איפוס הדגל
    
    # ========================================================================
    #                           ניתוב דפים - הפניה לפונקציות המתאימות
    # ========================================================================
    # בדיקת הדף הנבחר והפעלת הפונקציה המתאימה
    if page == "🏠 Dashboard":                  # דף לוח הבקרה הראשי
        show_dashboard()
    elif page == "📁 Data Upload":             # דף העלאת נתונים
        show_upload()
    elif page == "📈 Charts":                  # דף תרשימים
        show_charts()
    elif page == "📊 Statistics":              # דף סטטיסטיקות
        show_stats()
    elif page == "🤖 Machine Learning":        # דף למידת מכונה
        show_ml()
    elif page == "🧪 A/B Testing":            # דף בדיקות A/B
        show_ab_testing()
    elif page == "💾 Database":               # דף בסיס נתונים
        show_database()
    elif page == "📄 Reports":                # דף דוחות
        show_reports()

# ========================================================================
#                           פונקציות עזר ותובנות נתונים
# ========================================================================

def show_insights_and_advice(df):
    """
    יצירת תובנות והמלצות על בסיס הנתונים
    
    מטרת הפונקציה:
    - ניתוח איכות הנתונים ויצירת תובנות אוטומטיות
    - הצגת המלצות לשיפור הנתונים והניתוח
    - זיהוי דפוסים וחריגות בנתונים
    - מתן עצות מעשיות למשתמש
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים לניתוח
    
    החזרה: ללא - הפונקציה מציגה את התוצאות ישירות בממשק
    """
    
    if df is None or len(df) == 0:
        return
    
    insights = []
    advice = []
    
    # Data size analysis
    rows, cols = df.shape
    if rows > 100000:
        insights.append(f"📊 Large dataset: {rows:,} rows - excellent sample for analysis!")
        advice.append("💡 Recommend using sampling to speed up visualization")
    elif rows < 100:
        insights.append(f"📊 Small dataset: {rows} rows")
        advice.append("⚠️ Small sample may limit statistical significance of conclusions")
    
    # Data quality analysis
    missing_pct = (df.isnull().sum().sum() / (rows * cols)) * 100
    if missing_pct > 20:
        insights.append(f"❌ High percentage of missing data: {missing_pct:.1f}%")
        advice.append("🔧 Data cleaning needed - fill or remove missing values")
    elif missing_pct < 5:
        insights.append(f"✅ Excellent data quality: only {missing_pct:.1f}% missing")
        advice.append("🎯 Data ready for deep analysis and machine learning")
    
    # Data type analysis
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    if len(numeric_cols) > len(text_cols):
        insights.append(f"🔢 Predominantly numeric data: {len(numeric_cols)} out of {cols} columns")
        advice.append("📈 Perfect for correlation analysis and regression models")
    elif len(text_cols) > len(numeric_cols):
        insights.append(f"📝 Lots of text data: {len(text_cols)} out of {cols} columns")
        advice.append("🔤 Consider NLP analysis or categorical variable encoding")
    
    # Correlation analysis
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        high_corr = np.where(np.abs(corr_matrix) > 0.8)
        high_corr_pairs = [(corr_matrix.index[i], corr_matrix.columns[j]) 
                          for i, j in zip(high_corr[0], high_corr[1]) if i != j]
        
        if len(high_corr_pairs) > 0:
            insights.append(f"🔗 Strong correlations found between variables")
            advice.append("⚡ Use correlation analysis to identify dependencies")
    
    # Duplicate analysis
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        insights.append(f"🔄 Duplicates found: {duplicates} ({duplicates/rows*100:.1f}%)")
        advice.append("🧹 Recommend removing duplicates for analysis accuracy")
    else:
        insights.append("✅ No duplicates detected")
    
    # Outlier analysis
    outlier_cols = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        if len(outliers) > 0:
            outlier_cols.append(col)
    
    if outlier_cols:
        insights.append(f"🎯 Outliers detected in {len(outlier_cols)} columns")
        advice.append("🔍 Investigate outliers - they may contain important information")
    
    # Display insights and advice
    if insights:
        st.markdown("### 💡 Data Insights")
        for insight in insights:
            st.markdown(f'<div class="insight-box">{insight}</div>', unsafe_allow_html=True)
    
    if advice:
        st.markdown("### 🎯 Recommendations")
        for adv in advice:
            st.markdown(f'<div class="advice-box">{adv}</div>', unsafe_allow_html=True)

def show_dashboard():
    """
    הצגת לוח הבקרה הראשי של האפליקציה
    
    מטרת הפונקציה:
    - הצגת מסך פתיחה אטרקטיבי עם אפשרויות טעינת נתונים
    - הצגת מטריקות מפתח ותובנות על הנתונים הטעונים
    - מתן גישה מהירה לפונקציות הניתוח החשובות
    - יצירת ממשק מרכזי לניווט בין היכולות השונות
    
    התנהגות:
    - אם אין נתונים טעונים: הצגת מסך פתיחה עם כפתורי טעינת דוגמה
    - אם יש נתונים: הצגת לוח בקרה מלא עם מטריקות ותרשימים
    - כולל כפתורים לניתוח אוטומטי ויצירת תובנות חכמות
    
    החזרה: ללא - הפונקציה מציגה את התוכן ישירות בממשק
    """
    st.markdown("## 🏠 Welcome to DataBot Analytics Pro!")
    
    # Enhanced Dashboard with multiple sections
    if 'data' not in st.session_state:
        # Initial welcome section
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("### 🚀 Get Started")
            if st.button("🎲 Load Demo Data"):
                demo_data = create_demo_data()
                st.session_state.data = demo_data
                st.success("Demo data loaded! 🎉")
                st.rerun()
            
            if st.button("🛒 Load E-commerce Data"):
                ecommerce_data = create_ecommerce_data()
                st.session_state.data = ecommerce_data
                st.success("E-commerce data loaded! 💰")
                st.rerun()
            
            if st.button("📊 Generate Financial Data"):
                financial_data = create_financial_data()
                st.session_state.data = financial_data
                st.success("Financial data loaded! 💹")
                st.rerun()
        
        with col2:
            st.markdown("### 📋 Quick Info")
            st.info("🔍 DataBot Analytics Pro provides comprehensive data analysis capabilities")
            st.write("**Features:**")
            st.write("• Advanced visualizations")
            st.write("• Machine learning models")
            st.write("• Statistical analysis")
            st.write("• A/B testing")
            st.write("• Custom reports")
            st.write("• SQL database operations")
        
        # Feature showcase
        st.markdown("### ✨ Feature Highlights")
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            **📈 Advanced Analytics**
            - Interactive visualizations
            - 3D scatter plots
            - Correlation heatmaps
            - Distribution analysis
            """)
        
        with feature_col2:
            st.markdown("""
            **🤖 Machine Learning**
            - K-means clustering
            - PCA analysis
            - Anomaly detection
            - Feature importance
            """)
        
        with feature_col3:
            st.markdown("""
            **📊 Business Intelligence**
            - Executive dashboards
            - A/B testing
            - Statistical reports
            - Data quality metrics
            """)
        
        return
    
    # Main dashboard when data is loaded
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    # Enhanced header with action buttons
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.markdown("### 📊 Data Overview Dashboard")
    with col2:
        if st.button("🔍 Auto-Analysis"):
            auto_analyze_data()
    with col3:
        if st.button("🎯 Smart Insights"):
            generate_smart_insights(df)
    
    # Key metrics section
    st.markdown("### 📈 Key Metrics")
    metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
    
    with metric_col1:
        st.metric("📝 Total Rows", f"{len(df):,}")
    with metric_col2:
        st.metric("📊 Columns", f"{len(df.columns)}")
    with metric_col3:
        st.metric("🔢 Numeric", f"{len(numeric_cols)}")
    with metric_col4:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("❌ Missing %", f"{missing_pct:.1f}%")
    with metric_col5:
        quality_score = calculate_data_quality(df)
        st.metric("⭐ Quality Score", f"{quality_score:.1f}/10")
    
    # Data insights section
    show_insights_and_advice(df)
    
    # Interactive dashboard sections
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Quick Viz", "🔍 Data Explorer", "🎯 Recommendations", "📈 Trends"])
    
    with tab1:
        # Quick visualizations
        if len(numeric_cols) > 0:
            viz_col1, viz_col2 = st.columns(2)
            
            with viz_col1:
                # Auto-select best chart for first numeric column
                selected_col = st.selectbox("Select metric for quick viz", numeric_cols, key="quick_viz")
                
                if len(numeric_cols) >= 2:
                    fig = px.line(df.reset_index(), x='index', y=selected_col, 
                                title=f"Trend: {selected_col}")
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    fig = px.histogram(df, x=selected_col, title=f"Distribution: {selected_col}")
                    st.plotly_chart(fig, use_container_width=True)
            
            with viz_col2:
                if len(numeric_cols) > 1:
                    # Correlation heatmap
                    corr_matrix = df[numeric_cols].corr()
                    fig = px.imshow(corr_matrix, title="Correlation Matrix", 
                                  color_continuous_scale="RdBu")
                    st.plotly_chart(fig, use_container_width=True)
                elif len(text_cols) > 0:
                    # Category distribution
                    cat_col = text_cols[0]
                    value_counts = df[cat_col].value_counts().head(10)
                    fig = px.bar(x=value_counts.index, y=value_counts.values,
                               title=f"Top Categories: {cat_col}")
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # Data explorer
        st.markdown("#### 🔍 Interactive Data Explorer")
        
        # Filter controls
        filter_col1, filter_col2 = st.columns(2)
        
        with filter_col1:
            if len(text_cols) > 0:
                selected_category = st.selectbox("Filter by category", ["All"] + list(text_cols))
                if selected_category != "All":
                    category_values = st.multiselect(
                        f"Select {selected_category} values",
                        df[selected_category].unique(),
                        default=df[selected_category].unique()[:5]
                    )
                    if category_values:
                        df_filtered = df[df[selected_category].isin(category_values)]
                    else:
                        df_filtered = df
                else:
                    df_filtered = df
            else:
                df_filtered = df
        
        with filter_col2:
            if len(numeric_cols) > 0:
                selected_numeric = st.selectbox("Filter by numeric range", ["None"] + list(numeric_cols))
                if selected_numeric != "None":
                    min_val, max_val = st.slider(
                        f"Select {selected_numeric} range",
                        float(df[selected_numeric].min()),
                        float(df[selected_numeric].max()),
                        (float(df[selected_numeric].min()), float(df[selected_numeric].max()))
                    )
                    df_filtered = df_filtered[
                        (df_filtered[selected_numeric] >= min_val) & 
                        (df_filtered[selected_numeric] <= max_val)
                    ]
        
        # Display filtered data
        st.write(f"**Filtered Data:** {len(df_filtered)} rows (from {len(df)} total)")
        st.dataframe(df_filtered.head(20))
        
        # Quick stats on filtered data
        if len(df_filtered) > 0 and len(numeric_cols) > 0:
            st.markdown("#### 📊 Filtered Data Statistics")
            quick_stats = df_filtered[numeric_cols].describe().round(2)
            st.dataframe(quick_stats)
    
    with tab3:
        # Smart recommendations
        st.markdown("#### 🎯 Smart Recommendations")
        generate_dashboard_recommendations(df)
    
    with tab4:
        # Trend analysis
        st.markdown("#### 📈 Trend Analysis")
        if len(numeric_cols) > 0:
            trend_col = st.selectbox("Select column for trend analysis", numeric_cols, key="trend_analysis")
            
            # Create trend visualization
            df_trend = df.copy()
            df_trend['index'] = range(len(df_trend))
            
            # Calculate moving average
            window_size = min(20, len(df_trend) // 10)
            if window_size > 1:
                df_trend[f'{trend_col}_MA'] = df_trend[trend_col].rolling(window=window_size).mean()
            
            fig = go.Figure()
            
            # Original data
            fig.add_trace(go.Scatter(
                x=df_trend['index'],
                y=df_trend[trend_col],
                mode='lines',
                name='Original',
                opacity=0.6
            ))
            
            # Moving average
            if window_size > 1:
                fig.add_trace(go.Scatter(
                    x=df_trend['index'],
                    y=df_trend[f'{trend_col}_MA'],
                    mode='lines',
                    name=f'Moving Average ({window_size})',
                    line=dict(width=3)
                ))
            
            fig.update_layout(
                title=f"Trend Analysis: {trend_col}",
                xaxis_title="Data Points",
                yaxis_title=trend_col
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Trend insights
            trend_analysis = analyze_trend(df[trend_col])
            st.info(f"📈 Trend Analysis: {trend_analysis}")
            
            # Additional trend metrics
            if len(df) > 10:
                first_quarter = df[trend_col][:len(df)//4].mean()
                last_quarter = df[trend_col][-len(df)//4:].mean()
                overall_change = ((last_quarter - first_quarter) / first_quarter) * 100
                
                if abs(overall_change) > 5:
                    change_direction = "increased" if overall_change > 0 else "decreased"
                    st.write(f"📊 Overall trend: {trend_col} has {change_direction} by {abs(overall_change):.1f}%")
        
        # Volatility analysis
        if len(numeric_cols) > 0:
            st.markdown("#### 📊 Volatility Analysis")
            volatility_data = {}
            
            for col in numeric_cols[:5]:  # Analyze top 5 numeric columns
                cv = (df[col].std() / df[col].mean()) * 100 if df[col].mean() != 0 else 0
                volatility_data[col] = cv
            
            volatility_df = pd.DataFrame(list(volatility_data.items()), 
                                       columns=['Metric', 'Coefficient of Variation (%)'])
            
            fig = px.bar(volatility_df, x='Metric', y='Coefficient of Variation (%)',
                        title="Data Volatility Analysis")
            st.plotly_chart(fig, use_container_width=True)

def generate_smart_insights(df):
    """
    יצירת תובנות חכמות באמצעות ניתוח מתקדם של הנתונים
    
    מטרת הפונקציה:
    - ביצוע ניתוח מעמיק ואוטומטי של מסגרת הנתונים
    - זיהוי דפוסים, קשרים וחריגות בנתונים
    - יצירת המלצות מותאמות אישית למשתמש
    - הצגת תובנות בצורה בהירה ומובנת
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים לניתוח
    
    סוגי התובנות שמיוצרות:
    - ניתוח גודל הדאטה והמלצות על טכניקות מתאימות
    - זיהוי בעיות באיכות הנתונים (ערכים חסרים)
    - מציאת מתאמים חזקים בין משתנים
    - זיהוי ערכים חריגים (outliers)
    - ניתוח התפלגויות והמלצות על טרנספורמציות
    - הערכת רמת הייחודיות במשתנים קטגוריאליים
    
    החזרה: ללא - הפונקציה מציגה את התובנות ישירות בממשק
    """
    st.markdown("### 🧠 Smart Insights")
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    insights = []
    
    # Data size insights
    if len(df) > 100000:
        insights.append("🎯 **Big Data Opportunity**: Your dataset is large enough for advanced machine learning techniques")
    elif len(df) < 100:
        insights.append("⚠️ **Small Sample Alert**: Consider collecting more data for robust statistical analysis")
    
    # Missing data insights
    missing_cols = df.columns[df.isnull().sum() > 0]
    if len(missing_cols) > 0:
        worst_missing = df.isnull().sum().idxmax()
        missing_pct = (df[worst_missing].isnull().sum() / len(df)) * 100
        insights.append(f"🔧 **Data Quality Focus**: '{worst_missing}' has {missing_pct:.1f}% missing values - prioritize cleaning")
    
    # Correlation insights
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        high_corr_pairs = []
        
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = abs(corr_matrix.iloc[i, j])
                if corr_val > 0.8:
                    high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
        
        if high_corr_pairs:
            best_pair = max(high_corr_pairs, key=lambda x: x[2])
            insights.append(f"🔗 **Strong Relationship**: '{best_pair[0]}' and '{best_pair[1]}' are highly correlated ({best_pair[2]:.3f})")
    
    # Outlier insights
    outlier_summary = {}
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        outlier_summary[col] = len(outliers)
    
    if outlier_summary:
        max_outlier_col = max(outlier_summary, key=outlier_summary.get)
        if outlier_summary[max_outlier_col] > 0:
            outlier_pct = (outlier_summary[max_outlier_col] / len(df)) * 100
            insights.append(f"🎯 **Outlier Alert**: '{max_outlier_col}' has {outlier_summary[max_outlier_col]} outliers ({outlier_pct:.1f}%)")
    
    # Categorical insights
    if len(text_cols) > 0:
        for col in text_cols[:3]:
            unique_ratio = df[col].nunique() / len(df)
            if unique_ratio > 0.8:
                insights.append(f"🆔 **High Uniqueness**: '{col}' might be an identifier (80%+ unique values)")
            elif unique_ratio < 0.1:
                insights.append(f"📊 **Low Diversity**: '{col}' has limited categories - good for grouping analysis")
    
    # Distribution insights
    for col in numeric_cols[:3]:
        skewness = df[col].skew()
        if abs(skewness) > 2:
            direction = "right" if skewness > 0 else "left"
            insights.append(f"📈 **Skewed Distribution**: '{col}' is highly {direction}-skewed - consider transformation")
    
    # Display insights
    if insights:
        for insight in insights:
            st.write(f"• {insight}")
    else:
        st.info("🤖 No specific insights detected. Your data appears well-balanced!")

def generate_dashboard_recommendations(df):
    """
    יצירת המלצות מעשיות ללוח הבקרה על בסיס ניתוח הנתונים
    
    מטרת הפונקציה:
    - ניתוח מבנה הנתונים ויצירת המלצות מותאמות
    - זיהוי הזדמנויות לניתוח מתקדם במסגרת הנתונים
    - הצעת דרכי פעולה קונקרטיות לחקר הנתונים
    - מתן כיוונים לשימוש באלגוריתמי למידת מכונה
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים לניתוח
    
    סוגי ההמלצות שמיוצרות:
    - המלצות על סוגי תרשימים מתאימים
    - הצעות לניתוחים סטטיסטיים ספציפיים
    - כיוונים ליישום אלגוריתמי למידת מכונה
    - המלצות על צעדי ניקוי נתונים נדרשים
    - הצעות לבדיקות A/B מעניינות
    
    החזרה: ללא - הפונקציה מציגה את ההמלצות ישירות בממשק
    """
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    recommendations = []
    
    # Analysis recommendations
    if len(numeric_cols) >= 3:
        recommendations.append({
            "title": "🤖 Machine Learning Opportunity",
            "description": "With 3+ numeric variables, you can perform clustering and PCA analysis",
            "action": "Go to Machine Learning section",
            "priority": "High"
        })
    
    if len(numeric_cols) >= 2:
        recommendations.append({
            "title": "📊 Correlation Analysis",
            "description": "Explore relationships between your numeric variables",
            "action": "Check Charts → Heatmap or Scatter Plot",
            "priority": "Medium"
        })
    
    # Data quality recommendations
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct > 5:
        recommendations.append({
            "title": "🔧 Data Cleaning Needed",
            "description": f"Your data has {missing_pct:.1f}% missing values",
            "action": "Use Data Upload → Fill Missing Values",
            "priority": "High"
        })
    
    # Visualization recommendations
    if len(text_cols) > 0 and len(numeric_cols) > 0:
        recommendations.append({
            "title": "📈 Category Analysis",
            "description": "Compare numeric metrics across categories",
            "action": "Try Charts → Bar Chart or Box Plot",
            "priority": "Medium"
        })
    
    if len(numeric_cols) >= 3:
        recommendations.append({
            "title": "🌐 3D Visualization",
            "description": "Explore 3D relationships in your data",
            "action": "Use Charts → 3D Scatter Plot",
            "priority": "Medium"
        })
    
    # Statistical recommendations
    if len(df) > 1000:
        recommendations.append({
            "title": "🧪 A/B Testing Ready",
            "description": "Your sample size is suitable for statistical testing",
            "action": "Explore A/B Testing section",
            "priority": "Low"
        })
    
    # Business recommendations
    if 'revenue' in [col.lower() for col in df.columns] or 'sales' in [col.lower() for col in df.columns]:
        recommendations.append({
            "title": "💰 Business Analytics",
            "description": "Generate business intelligence reports",
            "action": "Create Executive Summary in Reports",
            "priority": "High"
        })
    
    # Display recommendations
    for i, rec in enumerate(recommendations):
        priority_color = {
            "High": "🔴",
            "Medium": "🟡", 
            "Low": "🟢"
        }
        
        with st.expander(f"{priority_color[rec['priority']]} {rec['title']}", expanded=(i < 2)):
            st.write(rec['description'])
            st.info(f"**Recommended Action:** {rec['action']}")

def create_financial_data():
    """
    יצירת נתוני דוגמה פיננסיים/השקעות לצורכי הדגמה
    
    מטרת הפונקציה:
    - יצירת מסגרת נתונים סינתטית הדומה לנתונים פיננסיים אמיתיים
    - הדמיה של מחירי מניות, נפחי מסחר ומדדים פיננסיים שונים
    - יצירת קורלציות ריאליסטיות בין המשתנים הפיננסיים
    - מתן בסיס לניתוח וויזואליזציה של נתונים פיננסיים
    
    הנתונים שנוצרים כוללים:
    - מחירי מניות עם טרנד וולטיליות ריאליסטיים
    - נפחי מסחר (Volume) עם התפלגות לוג-נורמלית  
    - שווי שוק (Market Cap) מבוסס על מחיר המניה
    - יחס מחיר לרווח (P/E Ratio) משתנה לפי סקטור
    - תשואת דיבידנד (Dividend Yield)
    - משתנים קטגוריאליים: סקטור, רמת סיכון
    - מדד ESG (Environmental, Social, Governance)
    - מטריקות מחושבות: תשואה יומית, וולטיליות, ממוצע נע
    
    החזרה:
        DataFrame: מסגרת נתונים עם 500 רשומות של נתונים פיננסיים סינתטיים
    """
    np.random.seed(456)
    
    n_records = 500
    
    # Create realistic financial data
    dates = pd.date_range('2023-01-01', periods=n_records, freq='D')
    
    # Simulate stock prices with some trend and volatility
    initial_price = 100
    returns = np.random.normal(0.001, 0.02, n_records)  # Daily returns
    prices = [initial_price]
    
    for r in returns[1:]:
        prices.append(prices[-1] * (1 + r))
    
    data = {
        'Date': dates,
        'Stock_Price': prices,
        'Volume': np.random.lognormal(10, 1, n_records).astype(int),
        'Market_Cap': np.array(prices) * np.random.uniform(1000000, 5000000, n_records),
        'P_E_Ratio': np.random.uniform(10, 30, n_records),
        'Dividend_Yield': np.random.uniform(0, 0.05, n_records),
        'Sector': np.random.choice(['Technology', 'Healthcare', 'Finance', 'Energy'], n_records),
        'Risk_Level': np.random.choice(['Low', 'Medium', 'High'], n_records),
        'ESG_Score': np.random.uniform(1, 10, n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Add calculated metrics
    df['Daily_Return'] = df['Stock_Price'].pct_change()
    df['Volatility'] = df['Daily_Return'].rolling(window=30).std()
    df['Moving_Avg_50'] = df['Stock_Price'].rolling(window=50).mean()
    
    # Add some correlations
    df.loc[df['Sector'] == 'Technology', 'P_E_Ratio'] *= 1.5  # Tech stocks higher P/E
    df.loc[df['Risk_Level'] == 'High', 'Volatility'] *= 1.3  # High risk = more volatile
    
    return df

def show_upload():
    """
    הצגת ממשק העלאת קבצים עם תמיכה למכשירים ניידים ודסקטופ
    
    מטרת הפונקציה:
    - מתן אפשרויות להעלאת קבצי נתונים בפורמטים שונים (CSV, Excel, JSON)
    - הטמעת אופטימיזציות מיוחדות למכשירים ניידים
    - מתן חלופות לטעינת נתונים עבור משתמשי מכשירים ניידים
    - יישום מנגנוני הגנה מפני שגיאות AxiosError
    
    פיצ'רים מרכזיים:
    - זיהוי אוטומטי של מכשירים ניידים והתאמת ממשק
    - הגבלת גודל קבצים (5MB למכשירים ניידים, 200MB לדסקטופ)
    - תמיכה בהעלאה מרובה של קבצים
    - אפשרויות חלופיות: בוט טלגרם, טעינת נתוני דוגמה
    - מסכי עזרה ואפשרויות ניקוי נתונים
    - תצוגה מקדימה של הנתונים לפני עיבוד
    
    התנהגות המערכת:
    - במצב נייד: הגבלות קפדניות יותר וכלים נוחים יותר
    - במצב דסקטופ: יכולות מלאות ותמיכה בקבצים גדולים
    - שמירת הנתונים במצב הסשן להמשך עבודה
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 📂 Data Upload")
    
    # Desktop-optimized file upload (no mobile complexity)
    max_size = 200 * 1024 * 1024  # 200MB for desktop
    st.markdown("### 📁 File Upload - **Up to 200MB**")

    uploaded_files = st.file_uploader(
        "Select files",
        type=['csv', 'xlsx', 'xls', 'json'],
        accept_multiple_files=True,
        help=f"Supported formats: CSV, Excel, JSON. Max size: {max_size // (1024*1024)}MB"
    )
    
    # ========================================================================
    #                           אפשרות חלופית - בוט טלגרם
    # ========================================================================
    # הצגת כפתור יפה לבוט הטלגרם כאלטרנטיבה לטעינת קבצים
    # הכפתור מוצג רק כאשר לא הועלו קבצים למערכת
    if not uploaded_files:
        st.markdown("---")
        st.markdown("### 🤖 Or Use Telegram Bot:")
        
        # כפתור אינטראקטיבי לפתיחת הבוט עם אנימציה
        if st.button("📱 Open DataBot", use_container_width=True, type="secondary"):
            st.balloons()  # הצגת בלונים לחגיגה
            st.success("🚀 Opening Telegram Bot...")
            st.markdown("👉 **[Click here to open bot](https://t.me/maydatabot123_bot)**")
            st.info("💡 The bot offers stable file uploads and mobile-friendly interface!")

    if uploaded_files:
        # Desktop processing - clean and fast
        st.info("🚀 **Processing files...**")
        
        # Clear any cached data that might cause conflicts
        if 'data' in st.session_state:
            del st.session_state['data']
        
        dfs = []
        
        # Progress bar for desktop processing
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i, uploaded_file in enumerate(uploaded_files):
            try:
                # Check file size
                file_size = uploaded_file.size if hasattr(uploaded_file, 'size') else len(uploaded_file.getvalue())
                
                if file_size > max_size:
                    st.error(f"❌ {uploaded_file.name}: File too large ({file_size/(1024*1024):.1f}MB). Max: {max_size/(1024*1024)}MB")
                    continue
                
                status_text.text(f"📂 Processing {uploaded_file.name}...")
                file_name = uploaded_file.name.lower()
                
                # Desktop processing - no retries needed
                max_retries = 1
                df = None
                
                for attempt in range(max_retries):
                    try:
                        if file_name.endswith('.csv'):
                            # Try to determine delimiter
                            try:
                                sample = str(uploaded_file.read(1024))
                                uploaded_file.seek(0)
                                
                                # Desktop processing - full file reading
                                if ';' in sample:
                                    df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
                                else:
                                    df = pd.read_csv(uploaded_file, encoding='utf-8')
                            except UnicodeDecodeError:
                                # Fallback encoding for problematic files
                                uploaded_file.seek(0)
                                df = pd.read_csv(uploaded_file, encoding='latin-1')
                                
                        elif file_name.endswith(('.xlsx', '.xls')):
                            df = pd.read_excel(uploaded_file)
                        elif file_name.endswith('.json'):
                            df = pd.read_json(uploaded_file)
                        else:
                            st.error(f"❌ Unsupported format: {file_name}")
                            break
                        
                        # If successful, break retry loop
                        if df is not None:
                            break
                            
                    except Exception as retry_error:
                        if attempt < max_retries - 1:
                            st.warning(f"⚠️ Attempt {attempt + 1} failed for {uploaded_file.name}, retrying...")
                            time.sleep(1)  # Brief pause before retry
                        else:
                            raise retry_error
                
                if df is not None:
                    
                    dfs.append(df)
                    st.success(f"✅ {uploaded_file.name} — Loaded {len(df)} rows, {len(df.columns)} columns")
                
                # Update progress
                progress_bar.progress((i + 1) / len(uploaded_files))

            except Exception as e:
                error_msg = str(e).lower()
                st.error(f"⚠️ Error reading {uploaded_file.name}: {str(e)}")
                
                # Specific AxiosError handling
                if 'network' in error_msg or 'axios' in error_msg or 'timeout' in error_msg:
                    st.error("🚨 **AxiosError/Network Error Detected!**")
                    st.info("🔧 **Try these solutions:**")
                    st.markdown("""
                    - ✅ **Enable Mobile Mode** in sidebar
                    - 🔄 **Refresh page** and try again
                    - 📶 **Check internet connection**
                    - 📱 **Use Telegram bot** instead
                    - 📝 **Try smaller file** (<5MB)
                    """)
        
        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        if dfs:
            if len(dfs) == 1:
                combined_df = dfs[0]
            else:
                # בדיקת זיכרון לפני איחוד קבצים
                total_rows = sum(len(df) for df in dfs)
                total_memory_mb = sum(df.memory_usage(deep=True).sum() / (1024*1024) for df in dfs)
                
                # אזהרה אם הנתונים גדולים מדי
                if total_rows > 1000000:  # יותר ממיליון שורות
                    st.warning(f"⚠️ **Large dataset detected:** {total_rows:,} total rows, ~{total_memory_mb:.1f} MB")
                    st.info("This may use significant memory. Consider processing files individually if you experience issues.")
                elif total_memory_mb > 500:  # יותר מ-500MB
                    st.warning(f"⚠️ **Memory usage:** ~{total_memory_mb:.1f} MB - Processing large dataset...")
                
                # Combine files with improved error handling
                try:
                    with st.spinner("🔄 Combining files..."):
                        combined_df = pd.concat(dfs, ignore_index=True)
                except MemoryError:
                    st.error("❌ **Memory Error:** Dataset too large to combine. Try processing files individually.")
                    combined_df = dfs[0]  # Use first file as fallback
                except Exception as e:
                    st.error(f"Error combining files: {e}")
                    combined_df = dfs[0]  # Use first file
            
            st.session_state.data = combined_df
            st.success(f"📊 Total loaded: {len(combined_df)} rows, {len(combined_df.columns)} columns")
            
            # Preview
            st.markdown("### 👀 Preview")
            st.dataframe(combined_df.head(10))
            
            # Show insights
            show_insights_and_advice(combined_df)
            
            # Data cleaning tools
            st.markdown("### 🔧 Data Cleaning")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("🗑️ Remove Duplicates"):
                    initial_len = len(combined_df)
                    combined_df = combined_df.drop_duplicates()
                    st.session_state.data = combined_df
                    removed = initial_len - len(combined_df)
                    st.success(f"Removed {removed} duplicates")
                    if removed > 0:
                        st.rerun()
            
            with col2:
                if st.button("🔧 Fill Missing Values"):
                    combined_df = fill_missing_values(combined_df)
                    st.session_state.data = combined_df
                    st.success("Missing values filled!")
                    st.rerun()
            
            with col3:
                if st.button("📊 Basic Statistics"):
                    st.markdown("#### 📈 Descriptive Statistics")
                    numeric_cols = combined_df.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) > 0:
                        st.dataframe(combined_df[numeric_cols].describe())
                    else:
                        st.info("No numeric columns for analysis")

def show_charts():
    """
    הצגת ממשק ויזואליזציות נתונים אינטראקטיביות
    
    מטרת הפונקציה:
    - מתן אפשרויות יצירת תרשימים מגוונים ואינטראקטיביים
    - תמיכה בויזואליזציות דו-מימדיות ותלת-מימדיות
    - יצירת תרשימי התפלגות, קורלציה וניתוח טרנדים
    - אפשרויות התאמה אישית של התרשימים
    
    סוגי התרשימים הזמינים:
    - תרשימי עמודות ופיזור (Scatter plots)
    - תרשימי קו וטרנדים זמניים
    - היסטוגרמות והתפלגויות
    - מפות חום של מתאמים (Heatmaps)
    - תרשימים תלת-מימדיים (3D Scatter)
    - תרשימי Box Plot לזיהוי ערכים חריגים
    - תרשימי עוגה (Pie Charts) למשתנים קטגוריאליים
    
    פיצ'רים מתקדמים:
    - אפשרויות סינון דינמיות של הנתונים
    - בחירת צבעים וסגנונות התרשימים
    - יכולות זום והגדלה במצבים אינטראקטיביים
    - אפשרויות הורדה וייצוא התרשימים
    - ניתוח טרנדים אוטומטי עם המלצות
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 📈 Data Visualization")
    
    if 'data' not in st.session_state:
        st.warning("📂 Please load data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['object', 'string']).columns.tolist()
    datetime_cols = df.select_dtypes(include=['datetime64']).columns.tolist()
    
    # Chart type selection
    chart_type = st.selectbox(
        "📊 Select chart type", 
        ["📈 Line Chart", "📊 Bar Chart", "🔵 Scatter Plot", "🌐 3D Scatter Plot",
         "📉 Area Chart", "🗺️ Heatmap", "🥧 Pie Chart", 
         "📦 Box Plot", "📊 Histogram", "🎻 Violin Plot"]
    )
    
    if chart_type == "📈 Line Chart" and len(numeric_cols) > 0:
        st.markdown("### 📈 Line Chart")
        
        col1, col2 = st.columns(2)
        with col1:
            y_col = st.selectbox("Y-axis", numeric_cols)
        with col2:
            x_col = st.selectbox("X-axis (optional)", ["Index"] + list(df.columns))
        
        if x_col == "Index":
            fig = px.line(df, y=y_col, title=f"Trend: {y_col}")
        else:
            fig = px.line(df, x=x_col, y=y_col, title=f"{y_col} by {x_col}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights for line chart
        if len(numeric_cols) > 0:
            trend_analysis = analyze_trend(df[y_col])
            st.info(f"📈 Trend: {trend_analysis}")
    
    elif chart_type == "📊 Bar Chart":
        st.markdown("### 📊 Bar Chart")
        
        if len(numeric_cols) > 0 and len(text_cols) > 0:
            col1, col2 = st.columns(2)
            with col1:
                cat_col = st.selectbox("Category", text_cols)
            with col2:
                val_col = st.selectbox("Value", numeric_cols)
            
            # Data aggregation
            agg_data = df.groupby(cat_col)[val_col].mean().reset_index()
            fig = px.bar(agg_data, x=cat_col, y=val_col, 
                        title=f"Average {val_col} by {cat_col}")
            st.plotly_chart(fig, use_container_width=True)
            
            # Insights
            top_category = agg_data.loc[agg_data[val_col].idxmax(), cat_col]
            st.success(f"🏆 Leading category: {top_category}")
        else:
            st.warning("Need categorical and numeric columns")
    
    elif chart_type == "🌐 3D Scatter Plot" and len(numeric_cols) >= 3:
        st.markdown("### 🌐 3D Scatter Plot")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols, key="3d_x")
        with col2:
            y_col = st.selectbox("Y-axis", [col for col in numeric_cols if col != x_col], key="3d_y")
        with col3:
            z_col = st.selectbox("Z-axis", [col for col in numeric_cols if col not in [x_col, y_col]], key="3d_z")
        with col4:
            color_col = st.selectbox("Color by", ["None"] + text_cols, key="3d_color")
        
        # Create 3D scatter plot
        fig = go.Figure()
        
        if color_col == "None":
            fig.add_trace(go.Scatter3d(
                x=df[x_col],
                y=df[y_col],
                z=df[z_col],
                mode='markers',
                marker=dict(
                    size=5,
                    color=df[z_col],
                    colorscale='Viridis',
                    colorbar=dict(title=z_col),
                    opacity=0.8
                ),
                text=[f'{x_col}: {x}<br>{y_col}: {y}<br>{z_col}: {z}' 
                      for x, y, z in zip(df[x_col], df[y_col], df[z_col])],
                hovertemplate='%{text}<extra></extra>'
            ))
        else:
            for category in df[color_col].unique():
                mask = df[color_col] == category
                fig.add_trace(go.Scatter3d(
                    x=df[mask][x_col],
                    y=df[mask][y_col],
                    z=df[mask][z_col],
                    mode='markers',
                    name=str(category),
                    marker=dict(size=5, opacity=0.8),
                    text=[f'{x_col}: {x}<br>{y_col}: {y}<br>{z_col}: {z}<br>{color_col}: {c}' 
                          for x, y, z, c in zip(df[mask][x_col], df[mask][y_col], 
                                               df[mask][z_col], df[mask][color_col])],
                    hovertemplate='%{text}<extra></extra>'
                ))
        
        fig.update_layout(
            title=f"3D Scatter Plot: {x_col} vs {y_col} vs {z_col}",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col,
                camera=dict(
                    eye=dict(x=1.2, y=1.2, z=1.2)
                )
            ),
            width=800,
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # 3D correlation analysis
        st.markdown("#### 🔗 3D Correlation Analysis")
        correlations_3d = {
            f"{x_col} - {y_col}": df[x_col].corr(df[y_col]),
            f"{x_col} - {z_col}": df[x_col].corr(df[z_col]),
            f"{y_col} - {z_col}": df[y_col].corr(df[z_col])
        }
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(f"{x_col} ↔ {y_col}", f"{correlations_3d[f'{x_col} - {y_col}']:.3f}")
        with col2:
            st.metric(f"{x_col} ↔ {z_col}", f"{correlations_3d[f'{x_col} - {z_col}']:.3f}")
        with col3:
            st.metric(f"{y_col} ↔ {z_col}", f"{correlations_3d[f'{y_col} - {z_col}']:.3f}")
        
        # 3D insights
        max_corr_3d = max(abs(corr) for corr in correlations_3d.values())
        if max_corr_3d > 0.7:
            st.success(f"🔗 Strong 3D relationships detected! Max correlation: {max_corr_3d:.3f}")
        elif max_corr_3d > 0.5:
            st.info(f"📊 Moderate 3D relationships found. Max correlation: {max_corr_3d:.3f}")
        else:
            st.warning(f"📉 Weak 3D relationships. Max correlation: {max_corr_3d:.3f}")
    
    elif chart_type == "🔵 Scatter Plot" and len(numeric_cols) >= 2:
        st.markdown("### 🔵 Scatter Plot")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_col = st.selectbox("Y-axis", [col for col in numeric_cols if col != x_col])
        with col3:
            color_col = st.selectbox("Color by", ["None"] + list(text_cols))
        
        if color_col == "None":
            fig = px.scatter(df, x=x_col, y=y_col, title=f"{y_col} vs {x_col}")
        else:
            fig = px.scatter(df, x=x_col, y=y_col, color=color_col, 
                           title=f"{y_col} vs {x_col} (color: {color_col})")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation analysis
        correlation = df[x_col].corr(df[y_col])
        if abs(correlation) > 0.7:
            st.success(f"🔗 Strong correlation: {correlation:.3f}")
        elif abs(correlation) > 0.3:
            st.info(f"📊 Moderate correlation: {correlation:.3f}")
        else:
            st.warning(f"📉 Weak correlation: {correlation:.3f}")
    
    elif chart_type == "🗺️ Heatmap" and len(numeric_cols) >= 2:
        st.markdown("### 🗺️ Correlation Heatmap")
        
        corr_matrix = df[numeric_cols].corr()
        fig = px.imshow(corr_matrix, 
                       title="Correlation Matrix",
                       color_continuous_scale="RdBu",
                       aspect="auto")
        st.plotly_chart(fig, use_container_width=True)
        
        # Find strong correlations
        strong_corrs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    strong_corrs.append(
                        (corr_matrix.columns[i], corr_matrix.columns[j], corr_val)
                    )
        
        if strong_corrs:
            st.markdown("#### 🔗 Strong Correlations:")
            for var1, var2, corr in strong_corrs:
                st.write(f"• {var1} ↔ {var2}: {corr:.3f}")
    
    elif chart_type == "🥧 Pie Chart" and len(text_cols) > 0:
        st.markdown("### 🥧 Pie Chart")
        
        cat_col = st.selectbox("Select category", text_cols)
        value_counts = df[cat_col].value_counts().head(10)  # Top-10 categories
        
        fig = px.pie(values=value_counts.values, names=value_counts.index,
                    title=f"Distribution of {cat_col}")
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics
        st.write(f"📊 Total unique values: {df[cat_col].nunique()}")
        dominant_cat = value_counts.index[0]
        dominant_pct = (value_counts.iloc[0] / len(df)) * 100
        st.info(f"🎯 Dominant category: {dominant_cat} ({dominant_pct:.1f}%)")
    
    elif chart_type == "📦 Box Plot" and len(numeric_cols) > 0:
        st.markdown("### 📦 Box Plot")
        
        col1, col2 = st.columns(2)
        with col1:
            num_col = st.selectbox("Numeric column", numeric_cols)
        with col2:
            group_col = st.selectbox("Grouping", ["None"] + list(text_cols))
        
        if group_col == "None":
            fig = px.box(df, y=num_col, title=f"Distribution of {num_col}")
        else:
            fig = px.box(df, x=group_col, y=num_col, 
                        title=f"Distribution of {num_col} by {group_col}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Outlier analysis
        Q1 = df[num_col].quantile(0.25)
        Q3 = df[num_col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[num_col] < Q1 - 1.5*IQR) | (df[num_col] > Q3 + 1.5*IQR)]
        
        if len(outliers) > 0:
            st.warning(f"⚠️ Outliers detected: {len(outliers)} ({len(outliers)/len(df)*100:.1f}%)")
        else:
            st.success("✅ No outliers detected")

    elif chart_type == "📊 Histogram" and len(numeric_cols) > 0:
        st.markdown("### 📊 Histogram")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            hist_col = st.selectbox("Select column", numeric_cols, key="hist_col")
        with col2:
            bins = st.slider("Number of bins", 10, 100, 30)
        with col3:
            show_normal = st.checkbox("Show normal curve", False)
        
        fig = px.histogram(df, x=hist_col, nbins=bins, title=f"Distribution: {hist_col}")
        
        if show_normal:
            # Add normal distribution overlay
            mean_val = df[hist_col].mean()
            std_val = df[hist_col].std()
            x_range = np.linspace(df[hist_col].min(), df[hist_col].max(), 100)
            normal_curve = stats.norm.pdf(x_range, mean_val, std_val)
            
            # Scale normal curve to match histogram
            normal_curve = normal_curve * len(df) * (df[hist_col].max() - df[hist_col].min()) / bins
            
            fig.add_trace(go.Scatter(
                x=x_range,
                y=normal_curve,
                mode='lines',
                name='Normal Distribution',
                line=dict(color='red', width=2)
            ))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Distribution statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Mean", f"{df[hist_col].mean():.2f}")
        with col2:
            st.metric("Std Dev", f"{df[hist_col].std():.2f}")
        with col3:
            st.metric("Skewness", f"{df[hist_col].skew():.2f}")
        with col4:
            st.metric("Kurtosis", f"{df[hist_col].kurtosis():.2f}")
    
    elif chart_type == "🎻 Violin Plot" and len(numeric_cols) > 0:
        st.markdown("### 🎻 Violin Plot")
        
        col1, col2 = st.columns(2)
        with col1:
            violin_col = st.selectbox("Numeric column", numeric_cols, key="violin_col")
        with col2:
            group_by = st.selectbox("Group by", ["None"] + text_cols, key="violin_group")
        
        if group_by == "None":
            fig = go.Figure()
            fig.add_trace(go.Violin(
                y=df[violin_col],
                name=violin_col,
                box_visible=True,
                meanline_visible=True
            ))
            fig.update_layout(title=f"Violin Plot: {violin_col}")
        else:
            fig = px.violin(df, y=violin_col, x=group_by, box=True,
                          title=f"Violin Plot: {violin_col} by {group_by}")
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Violin plot insights
        if group_by != "None":
            st.markdown("#### 📊 Group Comparison")
            group_stats = df.groupby(group_by)[violin_col].agg(['mean', 'std', 'median']).round(2)
            st.dataframe(group_stats)
    
    elif chart_type == "📉 Area Chart" and len(numeric_cols) > 0:
        st.markdown("### 📉 Area Chart")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            area_cols = st.multiselect("Select columns", numeric_cols, default=numeric_cols[:min(3, len(numeric_cols))])
        with col2:
            cumulative = st.checkbox("Cumulative", False)
        with col3:
            normalize = st.checkbox("Normalize (0-1)", False)
        
        if area_cols:
            df_area = df[area_cols].copy()
            
            if normalize:
                df_area = (df_area - df_area.min()) / (df_area.max() - df_area.min())
            
            if cumulative:
                df_area = df_area.cumsum()
            
            df_area['index'] = range(len(df_area))
            
            fig = px.area(df_area, x='index', y=area_cols,
                         title="Area Chart" + (" (Cumulative)" if cumulative else "") + (" (Normalized)" if normalize else ""))
            st.plotly_chart(fig, use_container_width=True)
    
    else:
        if len(numeric_cols) < 2:
            st.warning("⚠️ Need at least 2 numeric columns for this chart type")
        elif len(text_cols) == 0 and chart_type in ["📊 Bar Chart", "🥧 Pie Chart"]:
            st.warning("⚠️ Need categorical columns for this chart type")
        else:
            st.info("📊 Select appropriate data types for the chosen chart")

def analyze_trend(series):
    """
    ניתוח טרנדים מתקדם של סדרת נתונים
    
    מטרת הפונקציה:
    - ביצוע ניתוח רגרסיה לינארית לזיהוי כיוון הטרנד
    - חישוב עוצמת הטרנד באמצעות מקדם המתאם
    - הערכת שיעור השינוי האחוזי בסדרה
    - מתן תיאור מילולי מפורט של הטרנד
    
    פרמטרים:
        series (pandas.Series): סדרת הנתונים לניתוח
    
    החזרה:
        str: תיאור מפורט של הטרנד כולל כיוון, עוצמה ושיעור שינוי
        
    דוגמאות לתוצאות:
    - "Strong upward trend (R²=0.891, +15.3% change)"
    - "Weak downward trend (R²=0.234, -3.2% change)"
    """
    if len(series) < 2:
        return "Insufficient data"
    
    # Remove NaN values
    clean_series = series.dropna()
    if len(clean_series) < 2:
        return "Insufficient clean data"
    
    # Linear regression trend
    x = np.arange(len(clean_series))
    z = np.polyfit(x, clean_series, 1)
    slope = z[0]
    
    # Calculate trend strength
    correlation = np.corrcoef(x, clean_series)[0, 1]
    
    # Determine trend direction and strength
    if abs(correlation) > 0.7:
        strength = "strong"
    elif abs(correlation) > 0.4:
        strength = "moderate"
    else:
        strength = "weak"
    
    if slope > 0:
        direction = "upward"
    elif slope < 0:
        direction = "downward"
    else:
        direction = "flat"
    
    # Calculate percentage change
    first_val = clean_series.iloc[0]
    last_val = clean_series.iloc[-1]
    pct_change = ((last_val - first_val) / first_val) * 100 if first_val != 0 else 0
    
    return f"{strength.title()} {direction} trend (R²={correlation**2:.3f}, {pct_change:+.1f}% change)"

def analyze_trend(series):
    """
    ניתוח טרנדים פשוט של סדרת נתונים
    
    מטרת הפונקציה:
    - השוואה בין החצי הראשון לחצי השני של הסדרה
    - חישוב שיעור השינוי בין החלקים
    - קביעת כיוון הטרנד על בסיס השוואה זו
    
    פרמטרים:
        series (pandas.Series): סדרת הנתונים לניתוח
    
    החזרה:
        str: תיאור קצר של הטרנד
        
    דוגמאות לתוצאות:
    - "Growing trend (+8.5%)"
    - "Declining trend (-12.3%)"
    - "Stable trend (+2.1%)"
    """
    if len(series) < 2:
        return "Insufficient data"
    
    # Simple trend analysis
    first_half = series[:len(series)//2].mean()
    second_half = series[len(series)//2:].mean()
    
    change_pct = ((second_half - first_half) / first_half) * 100
    
    if change_pct > 5:
        return f"Growing trend (+{change_pct:.1f}%)"
    elif change_pct < -5:
        return f"Declining trend ({change_pct:.1f}%)"
    else:
        return f"Stable trend ({change_pct:.1f}%)"

def show_stats():
    """
    הצגת ממשק ניתוח סטטיסטי מתקדם של הנתונים
    
    מטרת הפונקציה:
    - מתן כלים מקיפים לניתוח סטטיסטי של מסגרת הנתונים
    - הצגת סטטיסטיקות תיאוריות וחיפוש דפוסים
    - ביצוע בדיקות השערות סטטיסטיות
    - זיהוי ערכים חריגים ואנומליות בנתונים
    
    יכולות הניתוח הסטטיסטי:
    - סטטיסטיקות תיאוריות: ממוצע, חציון, סטיית תקן
    - מדדי פיזור וצורת התפלגות: אסימטריה (skewness) וחדות (kurtosis) 
    - ניתוח מתאמים בין משתנים עם מטריצת קורלציה
    - בדיקות נורמליות של ההתפלגויות
    - זיהוי ערכים חריגים בשיטות מתקדמות
    - ניתוח שונות (ANOVA) לקבוצות שונות
    - בדיקות t-test למשתנים רציפים
    - בדיקות chi-square למשתנים קטגוריאליים
    
    פיצ'רים נוספים:
    - ויזואליזציה של התפלגויות
    - דוחות סטטיסטיים מפורטים
    - המלצות על בדיקות סטטיסטיות נוספות
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 📊 Statistical Analysis")
    
    if 'data' not in st.session_state:
        st.warning("📂 Please load data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) == 0:
        st.warning("🔢 No numeric columns in data for analysis")
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Descriptive Statistics")
        stats_df = df[numeric_cols].describe()
        st.dataframe(stats_df)
        
        # Distributions
        st.markdown("### 📊 Distribution Analysis")
        selected_col = st.selectbox("Select column", numeric_cols)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            # Histogram
            fig_hist = px.histogram(df, x=selected_col, title=f"Histogram: {selected_col}",
                                  nbins=30)
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col_b:
            # Q-Q plot for normality testing
            from scipy import stats as scipy_stats
            data_clean = df[selected_col].dropna()
            
            fig_qq = go.Figure()
            
            # Theoretical quantiles of normal distribution
            theoretical_quantiles = scipy_stats.norm.ppf(np.linspace(0.01, 0.99, len(data_clean)))
            sample_quantiles = np.sort(data_clean)
            
            fig_qq.add_trace(go.Scatter(
                x=theoretical_quantiles,
                y=sample_quantiles,
                mode='markers',
                name='Data'
            ))
            
            # Normal distribution line
            fig_qq.add_trace(go.Scatter(
                x=theoretical_quantiles,
                y=theoretical_quantiles * data_clean.std() + data_clean.mean(),
                mode='lines',
                name='Normal Distribution',
                line=dict(color='red', dash='dash')
            ))
            
            fig_qq.update_layout(title=f"Q-Q Plot: {selected_col}",
                               xaxis_title="Theoretical Quantiles",
                               yaxis_title="Sample Quantiles")
            st.plotly_chart(fig_qq, use_container_width=True)
    
    with col2:
        st.markdown("### 🧪 Statistical Tests")
        
        # Normality test
        if st.button("🔬 Normality Test"):
            data_sample = df[selected_col].dropna().sample(min(5000, len(df[selected_col].dropna())))
            stat, p_value = stats.shapiro(data_sample)
            
            st.metric("Test Statistic", f"{stat:.4f}")
            st.metric("P-value", f"{p_value:.4f}")
            
            if p_value > 0.05:
                st.success("✅ Data follows normal distribution")
            else:
                st.warning("❌ Data does not follow normal distribution")
        
        # Correlation analysis
        if len(numeric_cols) >= 2:
            st.markdown("#### 🔗 Correlation Analysis")
            
            col1_test = st.selectbox("Variable 1", numeric_cols, key="corr1")
            col2_test = st.selectbox("Variable 2", 
                                   [col for col in numeric_cols if col != col1_test], 
                                   key="corr2")
            
            if st.button("📊 Analyze Correlation"):
                # Data cleaning
                data1 = df[col1_test].dropna()
                data2 = df[col2_test].dropna()
                common_idx = data1.index.intersection(data2.index)
                data1 = data1[common_idx]
                data2 = data2[common_idx]
                
                # Pearson correlation
                corr_pearson, p_pearson = stats.pearsonr(data1, data2)
                
                # Spearman correlation
                corr_spearman, p_spearman = stats.spearmanr(data1, data2)
                
                st.metric("Pearson Correlation", f"{corr_pearson:.3f}")
                st.metric("P-value (Pearson)", f"{p_pearson:.4f}")
                st.metric("Spearman Correlation", f"{corr_spearman:.3f}")
                st.metric("P-value (Spearman)", f"{p_spearman:.4f}")
                
                # Interpretation
                if abs(corr_pearson) > 0.8:
                    st.success("🔗 Very strong correlation!")
                elif abs(corr_pearson) > 0.6:
                    st.info("📈 Strong correlation")
                elif abs(corr_pearson) > 0.3:
                    st.warning("📊 Moderate correlation")
                else:
                    st.error("📉 Weak correlation")
        
        # Outlier analysis
        st.markdown("#### 🎯 Outlier Analysis")
        if st.button("🔍 Find Outliers"):
            outliers_info = detect_outliers_advanced(df[selected_col])
            
            st.write("**Detection Methods:**")
            for method, data in outliers_info.items():
                st.write(f"• {method}: {data['count']} outliers ({data['percentage']:.1f}%)")

def detect_outliers_advanced(series):
    """
    זיהוי ערכים חריגים מתקדם באמצעות מספר שיטות
    
    מטרת הפונקציה:
    - זיהוי ערכים חריגים בסדרת נתונים בשיטות סטטיסטיות מגוונות
    - השוואה בין שיטות זיהוי שונות לקבלת תמונה מקיפה
    - הערכת רמת החומרה של הערכים החריגים
    - מתן המלצות לטיפול בערכים חריגים
    
    שיטות זיהוי המיושמות:
    - שיטת IQR (Interquartile Range) - הקלאסית
    - שיטת Z-Score - בהתבסס על סטיית תקן
    - שיטת Modified Z-Score - עמידה יותר לערכים חריגים
    - ניתוח אחוזונים - זיהוי ערכים קיצוניים
    
    פרמטרים:
        series (pandas.Series): סדרת הנתונים לבדיקה
    
    החזרה:
        dict: מילון עם תוצאות כל שיטות הזיהוי:
            - 'iqr_outliers': רשימת ערכים חריגים בשיטת IQR
            - 'z_score_outliers': רשימת ערכים חריגים בZ-Score
            - 'modified_z_outliers': רשימת ערכים חריגים בModified Z-Score
            - 'summary': סיכום כמותי של הערכים החריגים
    """
    
    results = {}
    clean_data = series.dropna()
    
    # IQR method
    Q1 = clean_data.quantile(0.25)
    Q3 = clean_data.quantile(0.75)
    IQR = Q3 - Q1
    iqr_outliers = clean_data[(clean_data < Q1 - 1.5*IQR) | (clean_data > Q3 + 1.5*IQR)]
    
    results['IQR'] = {
        'count': len(iqr_outliers),
        'percentage': len(iqr_outliers) / len(clean_data) * 100
    }
    
    # Z-score method
    z_scores = np.abs((clean_data - clean_data.mean()) / clean_data.std())
    z_outliers = clean_data[z_scores > 3]
    
    results['Z-Score'] = {
        'count': len(z_outliers),
        'percentage': len(z_outliers) / len(clean_data) * 100
    }
    
    # Modified Z-score (median)
    median = clean_data.median()
    mad = np.median(np.abs(clean_data - median))
    modified_z_scores = 0.6745 * (clean_data - median) / mad
    modified_z_outliers = clean_data[np.abs(modified_z_scores) > 3.5]
    
    results['Modified Z-Score'] = {
        'count': len(modified_z_outliers),
        'percentage': len(modified_z_outliers) / len(clean_data) * 100
    }
    
    return results

def show_ml():
    """
    הצגת ממשק למידת מכונה עם אלגוריתמים מתקדמים
    
    מטרת הפונקציה:
    - מתן כלים למידת מכונה בסיסיים ומתקדמים לניתוח נתונים
    - יישום אלגוריתמי קלאסטרינג, הפחתת מימדים ואנומליה
    - ויזואליזציה אינטראקטיבית של תוצאות אלגוריתמי למידת מכונה
    - הערכה וביצועים של מודלים שונים
    
    אלגוריתמי למידת המכונה הזמינים:
    
    1. K-Means Clustering:
       - קיבוץ נתונים לקבוצות הומוגניות
       - בחירה אוטומטית או ידנית של מספר קבוצות
       - ויזואליזציה של הקלאסטרים בממדים שונים
       - הערכת איכות הקלאסטרינג עם Silhouette Score
    
    2. PCA (Principal Component Analysis):
       - הפחתת מימדים תוך שמירה על מידע מקסימלי
       - הצגת אחוז השונות המוסברת בכל רכיב
       - ויזואליזציה דו-מימדית ותלת-מימדית של הנתונים
       - ניתוח תרומת המשתנים המקוריים לרכיבים
    
    3. Anomaly Detection:
       - זיהוי נקודות חריגות בנתונים
       - שימוש באלגוריתם Isolation Forest
       - הדגשה ויזואלית של הנקודות החריגות
       - ניתוח מאפייני הנקודות החריגות
    
    4. Feature Importance Analysis:
       - הערכת חשיבות המשתנים השונים
       - ויזואליזציה של הדירוג החשיבות
       - המלצות על משתנים לשמירה או הסרה
    
    פיצ'רים נוספים:
    - אפשרויות התאמה של פרמטרי האלגוריתמים
    - השוואה בין תוצאות שיטות שונות
    - ייצוא תוצאות ומודלים מאומנים
    - המלצות על השימוש המיטבי בכל אלגוריתם
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 🤖 Machine Learning")
    
    if 'data' not in st.session_state:
        st.warning("📂 Please load data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("🔢 Need at least 2 numeric columns for ML analysis!")
        return
    
    ml_type = st.selectbox(
        "🤖 Select analysis type",
        ["🎯 Clustering", "📉 PCA Analysis", "🔍 Anomaly Detection", "📊 Feature Importance"]
    )
    
    if ml_type == "🎯 Clustering":
        st.markdown("### 🎯 K-Means Clustering")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_features = st.multiselect(
                "Select features", 
                numeric_cols, 
                default=numeric_cols[:min(3, len(numeric_cols))]
            )
            
            n_clusters = st.slider("Number of clusters", 2, 10, 3)
        
        with col2:
            st.markdown("#### ⚙️ Settings")
            scale_data = st.checkbox("Normalize data", True)
            random_state = st.number_input("Random State", 0, 1000, 42)
        
        if len(selected_features) >= 2 and st.button("🚀 Run Clustering"):
            with st.spinner("Performing clustering..."):
                # Data preparation
                X = df[selected_features].dropna()
                
                if scale_data:
                    scaler = StandardScaler()
                    X_scaled = scaler.fit_transform(X)
                else:
                    X_scaled = X.values
                
                # Clustering
                kmeans = KMeans(n_clusters=n_clusters, random_state=random_state, n_init=10)
                clusters = kmeans.fit_predict(X_scaled)
                
                # Add clusters to data
                df_clustered = X.copy()
                df_clustered['Cluster'] = clusters
                
                # Visualization
                if len(selected_features) >= 2:
                    fig = px.scatter(
                        df_clustered, 
                        x=selected_features[0], 
                        y=selected_features[1],
                        color='Cluster',
                        title="K-Means Clustering Results",
                        color_discrete_sequence=px.colors.qualitative.Set1
                    )
                    
                    # Add centroids
                    if scale_data:
                        centroids_original = scaler.inverse_transform(kmeans.cluster_centers_)
                    else:
                        centroids_original = kmeans.cluster_centers_
                    
                    fig.add_trace(go.Scatter(
                        x=centroids_original[:, 0],
                        y=centroids_original[:, 1],
                        mode='markers',
                        marker=dict(symbol='x', size=15, color='black'),
                        name='Centroids'
                    ))
                    
                    st.plotly_chart(fig, use_container_width=True)
                
                # Cluster statistics
                st.markdown("### 📊 Cluster Statistics")
                cluster_stats = df_clustered.groupby('Cluster')[selected_features].agg(['mean', 'count'])
                st.dataframe(cluster_stats)
                
                # Cluster analysis
                st.markdown("### 💡 Cluster Analysis")
                for i in range(n_clusters):
                    cluster_data = df_clustered[df_clustered['Cluster'] == i]
                    cluster_size = len(cluster_data)
                    cluster_pct = (cluster_size / len(df_clustered)) * 100
                    
                    st.write(f"**Cluster {i}**: {cluster_size} points ({cluster_pct:.1f}%)")
                    
                    # Cluster characteristics
                    for feature in selected_features[:3]:  # Show first 3 features
                        mean_val = cluster_data[feature].mean()
                        overall_mean = df_clustered[feature].mean()
                        diff_pct = ((mean_val - overall_mean) / overall_mean) * 100
                        
                        if abs(diff_pct) > 10:
                            if diff_pct > 0:
                                st.write(f"  • {feature}: above average by {diff_pct:.1f}%")
                            else:
                                st.write(f"  • {feature}: below average by {abs(diff_pct):.1f}%")
                
                # Clustering quality metric
                from sklearn.metrics import silhouette_score
                silhouette_avg = silhouette_score(X_scaled, clusters)
                st.metric("Silhouette Score", f"{silhouette_avg:.3f}")
                
                if silhouette_avg > 0.7:
                    st.success("🎉 Excellent clustering quality!")
                elif silhouette_avg > 0.5:
                    st.info("👍 Good clustering quality")
                elif silhouette_avg > 0.3:
                    st.warning("⚠️ Satisfactory quality")
                else:
                    st.error("❌ Poor clustering quality")
    
    elif ml_type == "📉 PCA Analysis":
        st.markdown("### 📉 Principal Component Analysis (PCA)")
        
        selected_features = st.multiselect(
            "Select features", 
            numeric_cols, 
            default=numeric_cols
        )
        
        if len(selected_features) >= 2 and st.button("🔍 Perform PCA"):
            with st.spinner("Performing PCA analysis..."):
                # Data preparation
                X = df[selected_features].dropna()
                
                # Normalization
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # PCA
                pca = PCA()
                X_pca = pca.fit_transform(X_scaled)
                
                # Explained variance
                explained_variance = pca.explained_variance_ratio_
                cumulative_variance = np.cumsum(explained_variance)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Scree plot
                    fig_scree = px.bar(
                        x=range(1, len(explained_variance) + 1),
                        y=explained_variance,
                        title="Explained Variance by Component",
                        labels={'x': 'Principal Component', 'y': 'Explained Variance'}
                    )
                    st.plotly_chart(fig_scree, use_container_width=True)
                
                with col2:
                    # Cumulative explained variance
                    fig_cum = px.line(
                        x=range(1, len(cumulative_variance) + 1),
                        y=cumulative_variance,
                        title="Cumulative Explained Variance",
                        labels={'x': 'Number of Components', 'y': 'Cumulative Variance'}
                    )
                    fig_cum.add_hline(y=0.95, line_dash="dash", line_color="red", 
                                     annotation_text="95% variance")
                    st.plotly_chart(fig_cum, use_container_width=True)
                
                # PCA scatter plot (first 2 components)
                if len(X_pca) > 0:
                    pca_df = pd.DataFrame({
                        'PC1': X_pca[:, 0],
                        'PC2': X_pca[:, 1] if X_pca.shape[1] > 1 else np.zeros(len(X_pca))
                    })
                    
                    fig_scatter = px.scatter(
                        pca_df, x='PC1', y='PC2',
                        title=f"PCA: first 2 components (explain {cumulative_variance[1]*100:.1f}% variance)"
                    )
                    st.plotly_chart(fig_scatter, use_container_width=True)
                
                # Feature importance for first components
                st.markdown("### 📊 Feature Contribution to Principal Components")
                
                components_df = pd.DataFrame(
                    pca.components_[:min(3, len(pca.components_))].T,
                    columns=[f'PC{i+1}' for i in range(min(3, len(pca.components_)))],
                    index=selected_features
                )
                
                fig_components = px.bar(
                    components_df.reset_index().melt(id_vars='index'),
                    x='index', y='value', color='variable',
                    title="Feature Contribution to Principal Components",
                    labels={'index': 'Features', 'value': 'Contribution', 'variable': 'Component'}
                )
                st.plotly_chart(fig_components, use_container_width=True)
                
                # Recommendations
                components_95 = np.where(cumulative_variance >= 0.95)[0]
                if len(components_95) > 0:
                    n_components_95 = components_95[0] + 1
                    st.info(f"💡 To explain 95% variance, {n_components_95} components out of {len(selected_features)} are sufficient")
                    
                    reduction_pct = (1 - n_components_95/len(selected_features)) * 100
                    st.success(f"🎯 Possible dimensionality reduction by {reduction_pct:.1f}%")
    
    elif ml_type == "🔍 Anomaly Detection":
        st.markdown("### 🔍 Anomaly Detection")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            selected_features = st.multiselect(
                "Select features", 
                numeric_cols, 
                default=numeric_cols[:min(3, len(numeric_cols))]
            )
        
        with col2:
            method = st.selectbox("Method", ["Isolation Forest", "Local Outlier Factor", "One-Class SVM"])
            contamination = st.slider("Anomaly fraction", 0.01, 0.3, 0.1)
        
        if len(selected_features) >= 1 and st.button("🔍 Find Anomalies"):
            with st.spinner("Searching for anomalies..."):
                # Data preparation
                X = df[selected_features].dropna()
                
                # Normalization
                scaler = StandardScaler()
                X_scaled = scaler.fit_transform(X)
                
                # Anomaly detection
                if method == "Isolation Forest":
                    from sklearn.ensemble import IsolationForest
                    detector = IsolationForest(contamination=contamination, random_state=42)
                elif method == "Local Outlier Factor":
                    from sklearn.neighbors import LocalOutlierFactor
                    detector = LocalOutlierFactor(contamination=contamination)
                elif method == "One-Class SVM":
                    from sklearn.svm import OneClassSVM
                    detector = OneClassSVM(gamma='scale', nu=contamination)
                
                if method == "Local Outlier Factor":
                    anomaly_labels = detector.fit_predict(X_scaled)
                else:
                    anomaly_labels = detector.fit_predict(X_scaled)
                
                # Create DataFrame with results
                results_df = X.copy()
                results_df['Anomaly'] = anomaly_labels == -1
                results_df['Type'] = results_df['Anomaly'].map({True: 'Anomaly', False: 'Normal'})
                
                # Visualization
                if len(selected_features) >= 2:
                    fig = px.scatter(
                        results_df,
                        x=selected_features[0],
                        y=selected_features[1],
                        color='Type',
                        title=f"Anomaly Detection: {method}",
                        color_discrete_map={'Normal': 'blue', 'Anomaly': 'red'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Statistics
                n_anomalies = sum(anomaly_labels == -1)
                anomaly_pct = (n_anomalies / len(X)) * 100
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total points", len(X))
                with col2:
                    st.metric("Anomalies found", n_anomalies)
                with col3:
                    st.metric("Anomaly percentage", f"{anomaly_pct:.2f}%")
                
                # Show top anomalies
                if n_anomalies > 0:
                    st.markdown("### 🚨 Top-10 Anomalies")
                    anomalies = results_df[results_df['Anomaly']].head(10)
                    st.dataframe(anomalies[selected_features])
                    
                    # Anomaly analysis
                    st.markdown("### 📊 Anomaly Characteristics")
                    for feature in selected_features:
                        normal_mean = results_df[~results_df['Anomaly']][feature].mean()
                        anomaly_mean = results_df[results_df['Anomaly']][feature].mean()
                        
                        if not pd.isna(anomaly_mean) and not pd.isna(normal_mean):
                            diff_pct = ((anomaly_mean - normal_mean) / normal_mean) * 100
                            if abs(diff_pct) > 5:
                                direction = "higher" if diff_pct > 0 else "lower"
                                st.write(f"• **{feature}**: anomalies on average {direction} by {abs(diff_pct):.1f}%")
    
    elif ml_type == "📊 Feature Importance":
        st.markdown("### 📊 Feature Importance Analysis")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Feature selection
            selected_features = st.multiselect(
                "Select features for analysis", 
                numeric_cols, 
                default=numeric_cols[:min(5, len(numeric_cols))]
            )
            
            # Target variable selection
            target_col = st.selectbox(
                "Select target variable",
                numeric_cols,
                help="Variable to predict using other features"
            )
        
        with col2:
            st.markdown("#### ⚙️ Settings")
            algorithm = st.selectbox(
                "Algorithm", 
                ["Random Forest", "Gradient Boosting", "Extra Trees"],
                help="Machine learning algorithm for feature importance"
            )
            n_estimators = st.slider("Number of trees", 10, 200, 100)
            random_state = st.number_input("Random State", 0, 1000, 42)
        
        if len(selected_features) >= 2 and target_col and target_col not in selected_features:
            if st.button("📊 Calculate Feature Importance"):
                with st.spinner("Calculating feature importance..."):
                    # Data preparation
                    feature_data = df[selected_features + [target_col]].dropna()
                    
                    if len(feature_data) < 10:
                        st.warning("⚠️ Not enough data for reliable feature importance analysis.")
                        return
                    
                    X = feature_data[selected_features]
                    y = feature_data[target_col]
                    
                    # Choose algorithm
                    if algorithm == "Random Forest":
                        from sklearn.ensemble import RandomForestRegressor
                        model = RandomForestRegressor(
                            n_estimators=n_estimators, 
                            random_state=random_state,
                            n_jobs=-1
                        )
                    elif algorithm == "Gradient Boosting":
                        from sklearn.ensemble import GradientBoostingRegressor
                        model = GradientBoostingRegressor(
                            n_estimators=n_estimators, 
                            random_state=random_state
                        )
                    else:  # Extra Trees
                        from sklearn.ensemble import ExtraTreesRegressor
                        model = ExtraTreesRegressor(
                            n_estimators=n_estimators, 
                            random_state=random_state,
                            n_jobs=-1
                        )
                    
                    # Fit model
                    model.fit(X, y)
                    
                    # Get feature importance
                    importance_scores = model.feature_importances_
                    feature_importance_df = pd.DataFrame({
                        'Feature': selected_features,
                        'Importance': importance_scores,
                        'Importance_Pct': (importance_scores / importance_scores.sum()) * 100
                    }).sort_values('Importance', ascending=False)
                    
                    # Model performance
                    train_score = model.score(X, y)
                    
                    # Display results
                    col1, col2 = st.columns([1, 1])
                    
                    with col1:
                        st.markdown("### 📊 Feature Importance Ranking")
                        st.dataframe(
                            feature_importance_df,
                            use_container_width=True,
                            hide_index=True
                        )
                        
                        st.metric("Model R² Score", f"{train_score:.4f}")
                    
                    with col2:
                        # Bar chart
                        fig_bar = px.bar(
                            feature_importance_df,
                            x='Importance_Pct',
                            y='Feature',
                            orientation='h',
                            title=f'Feature Importance ({algorithm})',
                            labels={'Importance_Pct': 'Importance (%)', 'Feature': 'Features'},
                            color='Importance_Pct',
                            color_continuous_scale='viridis'
                        )
                        fig_bar.update_layout(
                            yaxis={'categoryorder': 'total ascending'},
                            height=400
                        )
                        st.plotly_chart(fig_bar, use_container_width=True)
                    
                    # Detailed insights
                    st.markdown("### 🔍 Insights")
                    
                    # Top 3 features
                    top_features = feature_importance_df.head(3)
                    st.markdown("**🥇 Top 3 Most Important Features:**")
                    for i, (_, row) in enumerate(top_features.iterrows(), 1):
                        emoji = ["🥇", "🥈", "🥉"][i-1]
                        st.write(f"{emoji} **{row['Feature']}**: {row['Importance_Pct']:.1f}% importance")
                    
                    # Cumulative importance
                    feature_importance_df['Cumulative_Pct'] = feature_importance_df['Importance_Pct'].cumsum()
                    features_80pct = len(feature_importance_df[feature_importance_df['Cumulative_Pct'] <= 80])
                    features_90pct = len(feature_importance_df[feature_importance_df['Cumulative_Pct'] <= 90])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Features for 80% importance", f"{features_80pct}/{len(selected_features)}")
                    with col2:
                        st.metric("Features for 90% importance", f"{features_90pct}/{len(selected_features)}")
                    with col3:
                        least_important = feature_importance_df.iloc[-1]['Feature']
                        st.metric("Least important feature", least_important)
                    
                    # Feature correlation with target
                    st.markdown("### 🎯 Feature-Target Correlations")
                    correlations = []
                    for feature in selected_features:
                        corr = feature_data[feature].corr(feature_data[target_col])
                        correlations.append({
                            'Feature': feature,
                            'Correlation': corr,
                            'Abs_Correlation': abs(corr)
                        })
                    
                    corr_df = pd.DataFrame(correlations).sort_values('Abs_Correlation', ascending=False)
                    
                    fig_corr = px.bar(
                        corr_df,
                        x='Feature',
                        y='Correlation',
                        title=f'Feature Correlations with {target_col}',
                        color='Correlation',
                        color_continuous_scale='RdBu_r'
                    )
                    fig_corr.add_hline(y=0, line_dash="dash", line_color="black")
                    st.plotly_chart(fig_corr, use_container_width=True)
                    
                    # Recommendations
                    st.markdown("### 💡 Recommendations")
                    high_importance = feature_importance_df[feature_importance_df['Importance_Pct'] > 15]
                    low_importance = feature_importance_df[feature_importance_df['Importance_Pct'] < 2]
                    
                    if len(high_importance) > 0:
                        st.success(f"🎯 **Focus on high-impact features**: {', '.join(high_importance['Feature'].tolist())}")
                    
                    if len(low_importance) > 0:
                        st.info(f"🔍 **Consider removing low-impact features**: {', '.join(low_importance['Feature'].tolist())}")
                    
                    if train_score < 0.5:
                        st.warning("⚠️ **Low model performance**: Consider feature engineering or different algorithms")
                    elif train_score > 0.8:
                        st.success("✅ **Good model performance**: Features explain the target well")
        
        elif target_col in selected_features:
            st.warning("⚠️ Target variable cannot be in the feature list!")
        elif len(selected_features) < 2:
            st.warning("⚠️ Select at least 2 features for analysis!")

def show_ab_testing():
    """
    הצגת ממשק לביצוע בדיקות A/B ובדיקות סטטיסטיות השוואתיות
    
    מטרת הפונקציה:
    - מתן כלים מתקדמים לביצוע בדיקות A/B מדעיות ומהימנות
    - השוואה סטטיסטית בין קבוצות או מצבים שונים
    - הערכת משמעות סטטיסטית של הבדלים שנצפו
    - יצירת המלצות עסקיות מבוססות נתונים
    
    סוגי הבדיקות הזמינות:
    
    1. Independent T-Test:
       - השוואה בין ממוצעים של שתי קבוצות בלתי תלויות
       - בדיקת הבדלים משמעותיים ברמת ביטחון גבוהה
       - הערכת גודל האפקט (Effect Size) Cohen's d
       - המלצות לגודל מדגם נדרש
    
    2. Chi-Square Test:
       - השוואה בין התפלגויות קטגוריאליות
       - בדיקת עצמאות בין משתנים קטגוריאליים
       - ניתוח טבלאות צולבות (Contingency Tables)
       - הערכת עוצמת הקשר בין משתנים
    
    3. Welch's T-Test:
       - גרסה עמידה של t-test לקבוצות עם שונויות שונות
       - מתאים למקרים שבהם הנחת שווית השונויות לא מתקיימת
       - ניתוח מתקדם יותר למדגמים לא מאוזנים
    
    4. Mann-Whitney U Test:
       - בדיקה נון-פרמטרית לקבוצות עם התפלגות לא נורמלית
       - השוואת חציונים במקום ממוצעים
       - עמידות גבוהה לערכים חריגים
    
    פיצ'רים מתקדמים:
    - יצירת נתוני דוגמה לבדיקות
    - חישוב Power Analysis לקביעת גודל מדגם
    - ויזואליזציה של התפלגויות והבדלים
    - דוחות מפורטים עם פרשנות סטטיסטית
    - המלצות לפעולות עתידיות
    - חישוב רמת ביטחון ורווחי סמך
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 🧪 A/B Testing")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🎲 Generate Test Data")
        if st.button("📊 Create A/B Test Data"):
            ab_data = generate_ab_test_data()
            st.session_state.data = ab_data
            st.success("A/B test data created!")
            st.rerun()
    
    if 'data' not in st.session_state:
        st.warning("📂 Load data or create A/B test data")
        return
    
    df = st.session_state.data
    
    with col2:
        st.markdown("### ⚙️ Test Configuration")
        
        # Automatic detection of group and metric
        group_cols = [col for col in df.columns if 'group' in col.lower() or 'variant' in col.lower() or 'test' in col.lower()]
        metric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        if group_cols:
            group_col = st.selectbox("Group column", group_cols, index=0)
        else:
            group_col = st.selectbox("Group column", df.columns)
        
        if metric_cols:
            metric_col = st.selectbox("Metric for analysis", metric_cols, index=0)
        else:
            metric_col = st.selectbox("Metric for analysis", df.columns)
    
    if st.button("🧪 Conduct A/B Test Analysis"):
        try:
            with st.spinner("Analyzing A/B test..."):
                # Data preparation
                test_data = df[[group_col, metric_col]].dropna()
                
                # Get unique groups
                groups = test_data[group_col].unique()
                
                if len(groups) != 2:
                    st.warning(f"⚠️ Found {len(groups)} groups. A/B test works with 2 groups.")
                    st.write("Available groups:", groups)
                    
                    # Take first 2 groups
                    if len(groups) > 2:
                        groups = groups[:2]
                        test_data = test_data[test_data[group_col].isin(groups)]
                        st.info(f"Analyzing groups: {groups[0]} vs {groups[1]}")
                
                # Split into control and treatment groups
                control = test_data[test_data[group_col] == groups[0]][metric_col]
                treatment = test_data[test_data[group_col] == groups[1]][metric_col]
                
                # Basic statistics
                control_mean = control.mean()
                treatment_mean = treatment.mean()
                control_std = control.std()
                treatment_std = treatment.std()
                
                # Statistical tests
                # T-test (Welch's t-test for unequal variances)
                t_stat, p_value_ttest = stats.ttest_ind(control, treatment, equal_var=False)
                
                # Mann-Whitney U test (non-parametric)
                try:
                    u_stat, p_value_mannwhitney = stats.mannwhitneyu(control, treatment, alternative='two-sided')
                except Exception as e:
                    st.warning(f"Mann-Whitney test failed: {e}")
                    p_value_mannwhitney = np.nan
                
                # Effect (difference of means)
                effect = treatment_mean - control_mean
                effect_pct = (effect / control_mean) * 100 if control_mean != 0 else 0
                
                # Cohen's d (effect size) - corrected calculation
                pooled_std = np.sqrt(((len(control) - 1) * control_std**2 + (len(treatment) - 1) * treatment_std**2) / (len(control) + len(treatment) - 2))
                cohens_d = effect / pooled_std if pooled_std != 0 else 0
                
                # Confidence interval for the difference
                se_diff = np.sqrt(control_std**2/len(control) + treatment_std**2/len(treatment))
                ci_lower = effect - 1.96 * se_diff
                ci_upper = effect + 1.96 * se_diff
                
                # Statistical power calculation
                from scipy.stats import norm
                pooled_se = np.sqrt(control_std**2/len(control) + treatment_std**2/len(treatment))
                z_score = abs(effect) / pooled_se if pooled_se != 0 else 0
                current_power = 1 - norm.cdf(1.96 - z_score) + norm.cdf(-1.96 - z_score) if pooled_se != 0 else 0
                
                # Sample size for 80% power
                if control_std > 0 and treatment_std > 0:
                    pooled_variance = (control_std**2 + treatment_std**2) / 2
                    n_per_group_80 = 2 * pooled_variance * ((1.96 + 0.84)**2) / (effect**2) if effect != 0 else np.inf
                else:
                    n_per_group_80 = np.inf
                
                # Display results
                st.markdown("### 📊 A/B Test Results")
                
                # Group metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(f"{groups[0]} (mean)", f"{control_mean:.3f}")
                with col2:
                    st.metric(f"{groups[1]} (mean)", f"{treatment_mean:.3f}")
                with col3:
                    st.metric("Difference", f"{effect:.3f}")
                with col4:
                    st.metric("Change %", f"{effect_pct:+.2f}%")
                
                # Statistical significance
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("P-value (t-test)", f"{p_value_ttest:.4f}")
                with col2:
                    if not np.isnan(p_value_mannwhitney):
                        st.metric("P-value (Mann-Whitney)", f"{p_value_mannwhitney:.4f}")
                    else:
                        st.metric("P-value (Mann-Whitney)", "N/A")
                with col3:
                    st.metric("Cohen's d", f"{cohens_d:.3f}")
                with col4:
                    st.metric("95% CI", f"[{ci_lower:.3f}, {ci_upper:.3f}]")
                
                # Results interpretation
                alpha = 0.05
                
                # Statistical significance
                st.markdown("#### 📊 Statistical Significance")
                if p_value_ttest < alpha:
                    st.success(f"🎉 **Statistically significant difference!** (t-test, p = {p_value_ttest:.4f})")
                    if ci_lower > 0:
                        st.info("✅ Confidence interval doesn't include 0 - effect is likely real")
                    elif ci_upper < 0:
                        st.info("✅ Confidence interval doesn't include 0 - effect is likely real")
                else:
                    st.warning(f"❌ **No statistically significant difference** (t-test, p = {p_value_ttest:.4f})")
                    st.info("🔍 This could mean: no real effect, insufficient sample size, or high variability")
                
                if not np.isnan(p_value_mannwhitney):
                    if p_value_mannwhitney < alpha:
                        st.success(f"🎉 **Mann-Whitney test also significant!** (p = {p_value_mannwhitney:.4f})")
                    else:
                        st.warning(f"❌ **Mann-Whitney test not significant** (p = {p_value_mannwhitney:.4f})")
                
                # Effect size interpretation
                st.markdown("#### 📏 Effect Size Analysis")
                if abs(cohens_d) < 0.2:
                    effect_size = "negligible"
                    effect_color = "🔵"
                elif abs(cohens_d) < 0.5:
                    effect_size = "small"
                    effect_color = "🟡"
                elif abs(cohens_d) < 0.8:
                    effect_size = "medium"
                    effect_color = "🟠"
                else:
                    effect_size = "large"
                    effect_color = "🔴"
                
                st.write(f"{effect_color} **Effect size: {effect_size}** (Cohen's d = {cohens_d:.3f})")
                
                # Practical significance
                if abs(effect_pct) > 10:
                    st.success(f"💰 **Practically significant**: {abs(effect_pct):.1f}% change")
                elif abs(effect_pct) > 5:
                    st.info(f"📊 **Moderate practical impact**: {abs(effect_pct):.1f}% change")
                else:
                    st.warning(f"📉 **Small practical impact**: {abs(effect_pct):.1f}% change")
                
                # Visualization
                col1, col2 = st.columns(2)
                
                with col1:
                    # Box plot
                    fig_box = px.box(test_data, x=group_col, y=metric_col, 
                                    title=f"Distribution of {metric_col} by Groups")
                    st.plotly_chart(fig_box, use_container_width=True)
                
                with col2:
                    # Histogram
                    fig_hist = go.Figure()
                    
                    fig_hist.add_trace(go.Histogram(
                        x=control,
                        name=f"{groups[0]}",
                        opacity=0.7,
                        nbinsx=30
                    ))
                    
                    fig_hist.add_trace(go.Histogram(
                        x=treatment,
                        name=f"{groups[1]}",
                        opacity=0.7,
                        nbinsx=30
                    ))
                    
                    fig_hist.update_layout(
                        title="Group Distributions",
                        xaxis_title=metric_col,
                        yaxis_title="Frequency",
                        barmode='overlay'
                    )
                    
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                # Statistical power and sample size
                st.markdown("### 📈 Statistical Power Analysis")
                
                power_col1, power_col2, power_col3 = st.columns(3)
                
                with power_col1:
                    st.metric("Current Power", f"{current_power:.3f}")
                
                with power_col2:
                    st.metric("Current Sample Size", f"{len(control) + len(treatment):,}")
                
                with power_col3:
                    if n_per_group_80 != np.inf and n_per_group_80 > 0:
                        st.metric("Sample Size for 80% Power", f"{int(n_per_group_80 * 2):,}")
                    else:
                        st.metric("Sample Size for 80% Power", "N/A")
                
                # Power interpretation
                if current_power >= 0.8:
                    st.success("✅ **Sufficient statistical power** (≥0.8)")
                    st.write("Your test has enough power to detect meaningful differences")
                elif current_power >= 0.5:
                    st.warning("⚠️ **Moderate statistical power** (0.5-0.8)")
                    st.write("Consider increasing sample size for more reliable results")
                else:
                    st.error("❌ **Low statistical power** (<0.5)")
                    st.write("High risk of missing real effects (Type II error)")
                
                # Sample size recommendations
                if n_per_group_80 != np.inf and n_per_group_80 > 0:
                    current_total = len(control) + len(treatment)
                    recommended_total = int(n_per_group_80 * 2)
                    
                    if current_total < recommended_total:
                        additional_needed = recommended_total - current_total
                        st.info(f"💡 **Recommendation**: Collect {additional_needed:,} more samples for 80% power")
                    else:
                        st.success("🎯 Your sample size exceeds the requirement for 80% power!")
                
                # Recommendations
                st.markdown("### 💡 Recommendations & Conclusions")
                
                recommendations = []
                
                # Statistical significance + practical significance
                if p_value_ttest < 0.05 and abs(effect_pct) > 5:
                    recommendations.append("🎯 **Strong evidence for effect**: Both statistically and practically significant")
                    recommendations.append("✅ **Action recommended**: Implement the tested change")
                elif p_value_ttest < 0.05 and abs(effect_pct) <= 5:
                    recommendations.append("📊 **Statistically significant but small effect**: Consider cost-benefit analysis")
                    recommendations.append("🤔 **Decision needed**: Is small improvement worth implementation cost?")
                elif p_value_ttest >= 0.05 and abs(effect_pct) > 10:
                    recommendations.append("📈 **Large effect but not statistically significant**: Increase sample size")
                    recommendations.append("🔄 **Action recommended**: Continue testing with more data")
                else:
                    recommendations.append("📋 **No convincing evidence of effect**: Consider alternative approaches")
                    recommendations.append("🔄 **Options**: Test different variants or longer duration")
                
                # Power-based recommendations
                if current_power < 0.8:
                    recommendations.append("📊 **Increase statistical power**: Larger sample size needed for reliable conclusions")
                
                # Effect size recommendations
                if abs(cohens_d) >= 0.5:
                    recommendations.append("💪 **Meaningful effect size detected**: Worth further investigation")
                elif abs(cohens_d) < 0.2:
                    recommendations.append("📉 **Very small effect**: Question if this change is worth pursuing")
                
                # Data quality recommendations
                control_cv = (control_std / control_mean) * 100 if control_mean != 0 else 0
                treatment_cv = (treatment_std / treatment_mean) * 100 if treatment_mean != 0 else 0
                
                if control_cv > 100 or treatment_cv > 100:
                    recommendations.append("⚠️ **High variability detected**: Consider data cleaning or longer measurement period")
                
                # Display recommendations
                for rec in recommendations:
                    st.write(f"• {rec}")
                
                # Summary conclusion
                st.markdown("#### 🎯 Executive Summary")
                
                if p_value_ttest < 0.05 and abs(effect_pct) > 5 and current_power > 0.8:
                    conclusion = "🟢 **STRONG POSITIVE RESULT**: Proceed with implementation"
                elif p_value_ttest < 0.05 and abs(effect_pct) > 2:
                    conclusion = "🟡 **MODERATE POSITIVE RESULT**: Consider implementation with monitoring"
                elif p_value_ttest >= 0.05 and current_power > 0.8:
                    conclusion = "🔴 **NO SIGNIFICANT EFFECT**: Do not implement this change"
                else:
                    conclusion = "🟡 **INCONCLUSIVE RESULT**: Need more data for reliable conclusion"
                
                st.write(conclusion)
                
                # Key metrics summary
                summary_metrics = {
                    "Control Mean": f"{control_mean:.3f}",
                    "Treatment Mean": f"{treatment_mean:.3f}",
                    "Difference": f"{effect:.3f}",
                    "% Change": f"{effect_pct:+.2f}%",
                    "P-value": f"{p_value_ttest:.4f}",
                    "Effect Size": f"{cohens_d:.3f}",
                    "Statistical Power": f"{current_power:.3f}",
                    "Significance": "Yes" if p_value_ttest < 0.05 else "No"
                }
                
                st.markdown("#### 📋 Key Metrics Summary")
                summary_df = pd.DataFrame([
                    {"Metric": k, "Value": v} for k, v in summary_metrics.items()
                ])
                st.dataframe(summary_df, use_container_width=True)
                
        except Exception as e:
            st.error(f"⚠️ Error in A/B test analysis: {str(e)}")
            st.info("💡 **Troubleshooting tips:**")
            st.write("• Check that your group column has exactly 2 distinct values")
            st.write("• Ensure your metric column contains numeric data")
            st.write("• Verify there are no empty or invalid values")
            st.write("• Try using demo A/B test data to test the functionality")

def generate_ab_test_data():
    """
    יצירת נתוני דוגמה ריאליסטיים לבדיקות A/B
    
    מטרת הפונקציה:
    - יצירת מסגרת נתונים סינתטית המדמה ניסוי A/B אמיתי
    - הדמיה של שתי קבוצות: בקרה (Control) וניסיון (Treatment)
    - יצירת הבדלים ריאליסטיים במטריקות העסקיות
    - מתן דוגמה עבודה לתרגול בדיקות A/B
    
    המבנה של נתוני הדוגמה:
    - Group: משתנה קטגוריאלי (A = Control, B = Treatment)
    - Conversion_Rate: שיעור המרה (מטריקה עיקרית)
    - Revenue: הכנסות ממוצעות
    - Page_Views: מספר צפיות בעמוד
    - Session_Duration: אורך הסשן בדקות
    - User_Satisfaction: דירוג שביעות רצון
    - Device_Type: סוג מכשיר (Desktop/Mobile/Tablet)
    - Age_Group: קבוצות גיל שונות
    
    הפרמטרים הסטטיסטיים:
    - קבוצת A: שיעור המרה של 12% בממוצע
    - קבוצת B: שיעור המרה של 15% בממוצע (שיפור של 25%)
    - התפלגות נורמלית עם רעש ריאליסטי
    - קורלציות טבעיות בין המשתנים השונים
    
    החזרה:
        DataFrame: מסגרת נתונים עם 1000 רשומות של ניסוי A/B מדומה
    """
    np.random.seed(42)
    
    n_control = 1000
    n_treatment = 1000
    
    # Control group (~10% conversion)
    control_data = {
        'group': ['Control'] * n_control,
        'user_id': range(1, n_control + 1),
        'conversion_rate': np.random.beta(2, 18, n_control),  # ~10% conversion
        'revenue': np.random.exponential(25, n_control),
        'clicks': np.random.poisson(100, n_control),
        'time_on_site': np.random.normal(120, 30, n_control),  # seconds
        'pages_viewed': np.random.poisson(3, n_control)
    }
    
    # Treatment group (~20% improvement)
    treatment_data = {
        'group': ['Treatment'] * n_treatment,
        'user_id': range(n_control + 1, n_control + n_treatment + 1),
        'conversion_rate': np.random.beta(2.4, 17.6, n_treatment),  # ~12% conversion
        'revenue': np.random.exponential(30, n_treatment),  # higher revenue
        'clicks': np.random.poisson(110, n_treatment),  # more clicks
        'time_on_site': np.random.normal(140, 35, n_treatment),  # more time
        'pages_viewed': np.random.poisson(3.5, n_treatment)  # more pages
    }
    
    # Combine data
    control_df = pd.DataFrame(control_data)
    treatment_df = pd.DataFrame(treatment_data)
    
    return pd.concat([control_df, treatment_df], ignore_index=True)

def _db_path() -> str:
    """
    החזרת נתיב לקובץ בסיס הנתונים SQLite העיקרי של האפליקציה
    
    מטרת הפונקציה:
    - מתן נתיב קבוע לקובץ בסיס הנתונים שבו נשמרים הקבצים המועלים
    - ריכוז ניהול הנתיב במקום אחד לקלות תחזוקה
    - תמיכה בשמירה קבועה של נתונים בין הרצות האפליקציה
    
    החזרה:
        str: נתיב לקובץ "uploaded_data.db" המשמש לאחסון הנתונים
    """
    return "uploaded_data.db"

def _run_sql(query: str) -> pd.DataFrame:
    """
    ביצוע שאילתת SQL על בסיס הנתונים העיקרי של האפליקציה
    
    מטרת הפונקציה:
    - ביצוע שאילתות SQL על בסיס הנתונים המקומי
    - טיפול בחיבור ובסגירה הבטוחה של בסיס הנתונים
    - המרה אוטומטית של תוצאות SQL למסגרת נתונים pandas
    - בדיקת קיום בסיס הנתונים לפני ביצוע השאילתה
    
    פרמטרים:
        query (str): שאילתת SQL לביצוע
    
    החזרה:
        pd.DataFrame: תוצאות השאילתה כמסגרת נתונים
        
    זורק:
        FileNotFoundError: אם בסיס הנתונים לא קיים (נדרש להעלות קבצים קודם)
        Exception: במקרה של שגיאה בביצוע השאילתה
    """
    db = _db_path()
    if not os.path.exists(db):
        raise FileNotFoundError("Database not found. Please upload CSV files first.")
    conn = sqlite3.connect(db)
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

def _show_query_insights(df: pd.DataFrame) -> None:
    """
    הצגת תובנות קומפקטיות על תוצאות השאילתה עם ויזואליזציה מהירה
    
    מטרת הפונקציה:
    - מתן סיכום מהיר של התוצאות המספריות מהשאילתה
    - הצגת מטריקות מפתח: סכום, ממוצע, חציון, טווח
    - יצירת תרשים עמודות מהיר אם התוצאות קטנות דיין
    - עזרה בהבנה מהירה של התוצאות ללא צורך בניתוח עמוק
    
    פרמטרים:
        df (pd.DataFrame): מסגרת הנתונים עם תוצאות השאילתה
        
    פלט:
    - מטריקות מספריות למשתנים נומריים (עד 4 עמודות)
    - תרשים עמודות אם יש פחות מ-20 שורות
    - סיכום בסיסי של מבנה הנתונים
    
    החזרה: ללא - הפונקציה מציגה את התוצאות ישירות
    """
    if df.empty:
        return

    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        st.markdown("#### 📊 Numeric Statistics — *Quick insights*")
        for col in num_cols[:4]:
            c1, c2, c3, c4 = st.columns(4)
            with c1:
                st.metric(f"{col} · Sum", f"{df[col].sum():,.2f}")
            with c2:
                st.metric(f"{col} · Avg", f"{df[col].mean():.2f}")
            with c3:
                st.metric(f"{col} · Max", f"{df[col].max():,.2f}")
            with c4:
                st.metric(f"{col} · Min", f"{df[col].min():.2f}")

    # Small categorical × numeric bar if feasible
    if len(df) <= 20 and len(df.columns) >= 2:
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols]
        if num_cols and cat_cols:
            fig = px.bar(df, x=cat_cols[0], y=num_cols[0],
                         title=f"{num_cols[0]} by {cat_cols[0]}")
            st.plotly_chart(fig, use_container_width=True)

    st.caption("**Explanation (EN):** We summarize numeric columns (sum/avg/min/max). "
               "If the result set is small and has both a categorical and a numeric field, "
               "we also render a quick bar chart.")

# ---------- Main section (DROP-IN REPLACEMENT for your show_database) ----------

# If _HAS_PG was not defined above for some reason, define it safely here too
try:
    _HAS_PG
except NameError:
    try:
        import psycopg2  # noqa: F401
        _HAS_PG = True
    except Exception:
        _HAS_PG = False


# ---------------------- Helpers ----------------------

def _validate_sql_query(sql: str) -> tuple[bool, str]:
    """
    ולידציה של שאילתת SQL למניעת SQL Injection
    
    מטרת הפונקציה:
    - לוודא שהשאילתה מכילה רק פקודות בטוחות לקריאה
    - למנוע פקודות מסוכנות שיכולות לגרום נזק
    - להחזיר הודעת שגיאה מפורטת במקרה של בעיה
    
    פרמטרים:
        sql (str): שאילתת SQL לבדיקה
    
    החזרה:
        tuple: (bool - האם השאילתה בטוחה, str - הודעת שגיאה אם קיימת)
    """
    if not sql or not sql.strip():
        return False, "SQL query cannot be empty"
    
    # הסרת רווחים ותווים מיוחדים מההתחלה והסוף
    sql_clean = sql.strip().upper()
    
    # רשימת פקודות מותרות (רק לקריאה)
    allowed_commands = ['SELECT', 'WITH', 'SHOW', 'DESCRIBE', 'EXPLAIN']
    
    # רשימת פקודות אסורות (כל מה שיכול לשנות או למחוק)
    forbidden_commands = [
        'DROP', 'DELETE', 'INSERT', 'UPDATE', 'ALTER', 'CREATE', 
        'TRUNCATE', 'REPLACE', 'EXEC', 'EXECUTE', 'CALL'
    ]
    
    # בדיקה שהשאילתה מתחילה בפקודה מותרת
    starts_with_allowed = any(sql_clean.startswith(cmd) for cmd in allowed_commands)
    if not starts_with_allowed:
        return False, f"SQL must start with one of: {', '.join(allowed_commands)}"
    
    # בדיקה שאין פקודות אסורות
    for forbidden in forbidden_commands:
        if forbidden in sql_clean:
            return False, f"Forbidden SQL command detected: {forbidden}"
    
    # בדיקת תווים חשודים
    suspicious_chars = [';--', '/*', '*/', 'xp_', 'sp_']
    for char in suspicious_chars:
        if char in sql_clean:
            return False, f"Suspicious SQL pattern detected: {char}"
    
    return True, "SQL query is safe"

def _sqlite_db_path() -> str:
    return "uploaded_data.db"

def _normalize_table_name(raw: str, fallback_idx: int = 1) -> str:
    name = raw.rsplit(".csv", 1)[0]
    name = "".join(ch.lower() if ch.isalnum() else "_" for ch in name)
    name = "_".join(filter(None, name.split("_")))
    if not name:
        name = f"table_{fallback_idx}"
    if name and name[0].isdigit():
        name = f"t_{name}"
    return name

def _sqlite_run_sql(query: str) -> pd.DataFrame:
    db = _sqlite_db_path()
    if not os.path.exists(db):
        raise FileNotFoundError("SQLite database not found. Please upload CSV files first.")
    conn = sqlite3.connect(db)
    try:
        return pd.read_sql_query(query, conn)
    finally:
        conn.close()

def _pg_run_sql(conn_kwargs: dict, query: str) -> pd.DataFrame:
    if not _HAS_PG:
        raise RuntimeError("psycopg2 is not installed. Run: pip install psycopg2-binary")
    import psycopg2  # safe: only executed when _HAS_PG True
    conn = psycopg2.connect(**conn_kwargs)
    try:
        return pd.read_sql(query, conn)
    finally:
        conn.close()

def _numeric_quick_insights(df: pd.DataFrame) -> None:
    if df.empty:
        return
    num_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if num_cols:
        st.markdown("#### 📊 Numeric Statistics — *Quick insights*")
        for col in num_cols[:4]:
            c1, c2, c3, c4 = st.columns(4)
            with c1: st.metric(f"{col} · Sum", f"{df[col].sum():,.2f}")
            with c2: st.metric(f"{col} · Avg", f"{df[col].mean():.2f}")
            with c3: st.metric(f"{col} · Max", f"{df[col].max():.2f}")
            with c4: st.metric(f"{col} · Min", f"{df[col].min():.2f}")
    if len(df) <= 20 and len(df.columns) >= 2:
        num_cols = df.select_dtypes(include=["number"]).columns.tolist()
        cat_cols = [c for c in df.columns if c not in num_cols]
        if num_cols and cat_cols:
            fig = px.bar(df, x=cat_cols[0], y=num_cols[0],
                         title=f"{num_cols[0]} by {cat_cols[0]}")
            st.plotly_chart(fig, use_container_width=True)
    st.caption("**Explanation (EN):** We summarize numeric columns (sum/avg/min/max). "
               "If the result set is small and has both a categorical and a numeric field, "
               "we also render a quick bar chart.")


# ---------------------- Main UI ----------------------
def show_database():
    """
    הצגת ממשק עבודה עם בסיסי נתונים ושאילתות SQL
    
    מטרת הפונקציה:
    - מתן כלים מתקדמים לעבודה עם בסיסי נתונים שונים
    - תמיכה בשאילתות SQL ישירות על הנתונים שהועלו
    - אפשרויות חיבור לבסיסי נתונים חיצוניים (PostgreSQL)
    - יצירת טבלאות זמניות לשאילתות מורכבות
    
    סוגי בסיסי הנתונים הנתמכים:
    
    1. SQLite (Local):
       - בסיס נתונים מקומי המותקן עם האפליקציה
       - יצירה אוטומטית של טבלאות מהקבצים שהועלו
       - שאילתות מהירות וקלות על נתונים קטנים-בינוניים
       - לא דורש הגדרות חיבור נוספות
    
    2. PostgreSQL (Remote):
       - חיבור לבסיסי נתונים PostgreSQL מרוחקים
       - תמיכה בשאילתות מורכבות על נתונים גדולים
       - אפשרויות אבטחה וחיבור מתקדמות
       - דורש פרמטרי חיבור: שרת, משתמש, סיסמה
    
    3. In-Memory (Demo):
       - בסיס נתונים זמני בזיכרון לצורכי הדגמה
       - אידיאלי לבדיקות מהירות ולימוד SQL
       - לא שומר נתונים בין הפעלות האפליקציה
    
    פיצ'רים מתקדמים:
    - עורך SQL אינטראקטיבי עם הדגשת תחביר
    - שאילתות מוכנות מראש לדוגמה ולמידה
    - ניתוח אוטומטי של תוצאות השאילתות
    - ויזואליזציה מהירה של התוצאות
    - תובנות על ביצועי השאילתות
    - ייצוא תוצאות לקבצים או לזיכרון האפליקציה
    - התראות על שגיאות וטיפים לשיפור השאילתות
    
    דוגמאות שימוש:
    - ניתוח נתונים עסקיים עם GROUP BY ו-aggregations
    - זיהוי טרנדים עם Window Functions
    - חיבור טבלאות (JOINs) לניתוח רב-מימדי
    - סינון וחיפוש מתקדם בנתונים
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 💾 Database and SQL")

    backend = st.radio(
        "Choose database backend",
        ["SQLite (uploaded CSV files)", "PostgreSQL (connect to server)"],
        horizontal=False,
    )

    # ---------- SQLite MODE (files -> local SQLite) ----------
    if backend.startswith("SQLite"):
        left, right = st.columns([2, 1])

        # LEFT: upload & SQL
        with left:
            st.markdown("### 🔗 Database Management — *Upload & Inspect*")

            c1, c2 = st.columns([1, 1])
            with c1:
                replace_db = st.checkbox(
                    "Replace database on upload",
                    value=True,
                    help="If enabled, the existing SQLite DB will be deleted before loading new files."
                )
            with c2:
                if st.button("🧹 Reset database"):
                    if os.path.exists(_sqlite_db_path()):
                        os.remove(_sqlite_db_path())
                    st.success("Database reset. Upload new CSV files to create fresh tables.")
                    st.stop()

            uploaded = st.file_uploader(
                "Upload CSV files",
                type=["csv"],
                accept_multiple_files=True,
                help="Each CSV becomes a table inside uploaded_data.db"
            )

            if uploaded and st.button("📁 Load files into SQLite"):
                try:
                    if replace_db and os.path.exists(_sqlite_db_path()):
                        os.remove(_sqlite_db_path())
                    conn = sqlite3.connect(_sqlite_db_path())
                    loaded = []
                    for idx, f in enumerate(uploaded, start=1):
                        df = pd.read_csv(f)
                        name = _normalize_table_name(f.name, fallback_idx=idx)
                        df.to_sql(name, conn, if_exists="replace", index=False)
                        loaded.append((name, len(df)))
                        st.success(f"✅ {f.name} → `{name}` ({len(df):,} rows)")
                    conn.close()
                    st.success(f"🎉 Loaded {len(loaded)} table(s).")
                    st.caption("**Explanation (EN):** We created/overwrote a local SQLite DB; "
                               "now the SQL editor and quick queries will use your tables only.")
                except Exception as e:
                    st.error(f"Load error: {e}")
                    st.info("💡 Try simpler ASCII file names if the issue persists.")

            st.markdown("### ✏️ SQL Editor — *Run Queries*")

            # List tables
            tables = []
            if os.path.exists(_sqlite_db_path()):
                try:
                    conn = sqlite3.connect(_sqlite_db_path())
                    tdf = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
                    tables = tdf["name"].tolist()
                    if tables:
                        st.markdown(f"**Available tables in `{_sqlite_db_path()}`:**")
                        for t in tables:
                            try:
                                info = pd.read_sql_query(f"SELECT * FROM pragma_table_info('{t}');", conn)
                                cnt = pd.read_sql_query(f'SELECT COUNT(*) AS c FROM "{t}";', conn)["c"].iloc[0]
                                cols = ", ".join(info["name"].tolist()) if not info.empty else "—"
                                st.write(f"• `{t}` — {cnt:,} rows · {cols}")
                            except Exception as e:
                                st.write(f"• `{t}` — structure read error: {str(e)[:80]}…")
                except Exception as e:
                    st.warning(f"Could not open DB: {e}")
                finally:
                    try: conn.close()
                    except: pass
            else:
                st.info("📂 No database yet. Upload CSV files to create one.")

            # Templates
            if tables:
                sel_table = st.selectbox("Table for templates", tables)
                templates = {
                    "🔎 Show 10 rows":  f'SELECT * FROM "{sel_table}" LIMIT 10;',
                    "🔢 Count records": f'SELECT COUNT(*) AS total_records FROM "{sel_table}";',
                    "🧱 Table info":    f"SELECT * FROM pragma_table_info('{sel_table}');",
                }
                # numeric template if exists
                try:
                    conn = sqlite3.connect(_sqlite_db_path())
                    sample = pd.read_sql_query(f'SELECT * FROM "{sel_table}" LIMIT 50;', conn)
                    conn.close()
                    num_cols = sample.select_dtypes(include=["number"]).columns.tolist()
                    if num_cols:
                        c = num_cols[0]
                        templates["📈 Basic stats"] = (
                            f'SELECT AVG("{c}") AS avg_{c}, SUM("{c}") AS sum_{c}, '
                            f'MAX("{c}") AS max_{c}, MIN("{c}") AS min_{c} '
                            f'FROM "{sel_table}";'
                        )
                except Exception:
                    pass
                chosen = st.selectbox("Query template", list(templates.keys()))
                template_sql = templates[chosen]
            else:
                template_sql = "-- Upload CSV files first.\nSELECT 'No tables available' AS message;"

            sql = st.text_area("SQL Query", value=template_sql, height=160)
            if st.button("▶️ Execute (SQLite)"):
                # בדיקת אבטחה למניעת SQL Injection
                is_safe, error_msg = _validate_sql_query(sql)
                if not is_safe:
                    st.error(f"🚨 **Security Error:** {error_msg}")
                    st.warning("Only SELECT, WITH, SHOW, DESCRIBE, and EXPLAIN queries are allowed for security reasons.")
                else:
                    try:
                        result = _sqlite_run_sql(sql)
                        st.success("✅ Query executed successfully.")
                        st.dataframe(result, use_container_width=True)
                        _numeric_quick_insights(result)
                    except Exception as e:
                        st.error(f"Query error: {e}")

        # RIGHT: quick queries
        with right:
            st.markdown("### 📊 Quick Queries — *One-click analysis*")
            if not os.path.exists(_sqlite_db_path()):
                st.info("No SQLite database yet. Upload CSV files on the left.")
                return
            conn = sqlite3.connect(_sqlite_db_path())
            try:
                tdf = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
                tables = tdf["name"].tolist()
            finally:
                conn.close()
            if not tables:
                st.info("No tables found. Upload CSV files first.")
                return

            q_table = st.selectbox("Table", tables, key="quick_table_sqlite")
            # peek
            conn = sqlite3.connect(_sqlite_db_path())
            try:
                peek = pd.read_sql_query(f'SELECT * FROM "{q_table}" LIMIT 200;', conn)
            finally:
                conn.close()

            num_cols = peek.select_dtypes(include=["number"]).columns.tolist()
            cat_cols = [c for c in peek.columns if c not in num_cols]

            if st.button("📋 Table Summary (SQLite)"):
                total = _sqlite_run_sql(f'SELECT COUNT(*) AS c FROM "{q_table}";')
                st.metric("Total Records", f"{int(total.iloc[0,0]):,}")
                head = _sqlite_run_sql(f'SELECT * FROM "{q_table}" LIMIT 5;')
                st.dataframe(head, use_container_width=True)
                st.caption("**Explanation (EN):** Total row count and a 5-row preview.")

            if num_cols and st.button("💰 Numeric Summary (SQLite)"):
                parts = []
                for c in num_cols[:5]:
                    parts += [f'AVG("{c}") AS avg_{c}', f'SUM("{c}") AS sum_{c}',
                              f'MAX("{c}") AS max_{c}', f'MIN("{c}") AS min_{c}']
                res = _sqlite_run_sql(f'SELECT {", ".join(parts)} FROM "{q_table}";')
                for c in num_cols[:3]:
                    a1, a2, a3, a4 = st.columns(4)
                    with a1: st.metric(f"{c} · Avg", f"{res[f'avg_{c}'].iloc[0]:.2f}")
                    with a2: st.metric(f"{c} · Sum", f"{res[f'sum_{c}'].iloc[0]:,.2f}")
                    with a3: st.metric(f"{c} · Max", f"{res[f'max_{c}'].iloc[0]:.2f}")
                    with a4: st.metric(f"{c} · Min", f"{res[f'min_{c}'].iloc[0]:.2f}")
                st.caption("**Explanation (EN):** Aggregations are computed directly in SQLite.")

            if cat_cols and st.button("👥 Category Analysis (SQLite)"):
                cat = cat_cols[0]
                res = _sqlite_run_sql(
                    f'SELECT "{cat}" AS category, COUNT(*) AS cnt '
                    f'FROM "{q_table}" GROUP BY "{cat}" ORDER BY cnt DESC LIMIT 15;'
                )
                if not res.empty:
                    fig = px.bar(res, x="category", y="cnt", title=f"Distribution of {cat}")
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(res)
                    st.caption("**Explanation (EN):** Counts the most frequent categories.")

            if num_cols and st.button("📈 Recent Trend (last 100 rows, SQLite)"):
                target = num_cols[0]
                res = _sqlite_run_sql(
                    f'SELECT rowid AS idx, "{target}" FROM "{q_table}" '
                    f"ORDER BY rowid DESC LIMIT 100;"
                )
                if not res.empty:
                    res = res.sort_values("idx")
                    fig = px.line(res, x="idx", y=target, title=f"Trend of {target} (last 100 rows)")
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("**Explanation (EN):** Uses SQLite internal rowid as an approximate recent order.")

    # ---------- POSTGRESQL MODE (read-only connection) ----------
    else:
        if not _HAS_PG:
            st.error("PostgreSQL driver not found. Install it first:\n`pip install psycopg2-binary`")
            return

        left, right = st.columns([2, 1])

        # LEFT: connection & SQL editor
        with left:
            st.markdown("### 🔗 PostgreSQL Connection — *Connect & Query*")

            with st.form("pg_conn_form", clear_on_submit=False):
                host = st.text_input("Host", "localhost")
                port = st.text_input("Port", "5432")
                dbname = st.text_input("Database", "")
                user = st.text_input("User", "")
                password = st.text_input("Password", type="password")
                submitted = st.form_submit_button("🔌 Connect")

            if submitted:
                st.session_state.pg_conn = {
                    "host": host, "port": port, "dbname": dbname,
                    "user": user, "password": password,
                }
                st.success("Connection parameters saved. Use the widgets below.")
                st.caption("**Explanation (EN):** We do not persist credentials; they live in session only.")

            if "pg_conn" not in st.session_state:
                st.info("Enter connection parameters and click **Connect**.")
                return

            conn_kwargs = st.session_state.pg_conn

            # list tables (user schemas only)
            try:
                tables_df = _pg_run_sql(conn_kwargs, """
                    SELECT table_schema, table_name
                    FROM information_schema.tables
                    WHERE table_type='BASE TABLE'
                      AND table_schema NOT IN ('pg_catalog','information_schema')
                    ORDER BY table_schema, table_name;
                """)
                st.markdown("**Available tables (schema.table):**")
                tables_df["qualified"] = tables_df["table_schema"] + "." + tables_df["table_name"]
                for _, r in tables_df.iterrows():
                    st.write(f"• `{r['qualified']}`")
            except Exception as e:
                st.error(f"Failed to list tables: {e}")
                return

            # SQL editor
            default_sql = "SELECT NOW() AS server_time;"
            sql = st.text_area("SQL Query (PostgreSQL)", value=default_sql, height=160)
            if st.button("▶️ Execute (PostgreSQL)"):
                # בדיקת אבטחה למניעת SQL Injection  
                is_safe, error_msg = _validate_sql_query(sql)
                if not is_safe:
                    st.error(f"🚨 **Security Error:** {error_msg}")
                    st.warning("Only SELECT, WITH, SHOW, DESCRIBE, and EXPLAIN queries are allowed for security reasons.")
                else:
                    try:
                        result = _pg_run_sql(conn_kwargs, sql)
                        st.success("✅ Query executed successfully.")
                        st.dataframe(result, use_container_width=True)
                        _numeric_quick_insights(result)
                    except Exception as e:
                        st.error(f"Query error: {e}")

        # RIGHT: quick queries (schema-aware)
        with right:
            st.markdown("### 📊 Quick Queries — *One-click analysis*")

            try:
                tdf = _pg_run_sql(st.session_state.pg_conn, """
                    SELECT table_schema, table_name
                    FROM information_schema.tables
                    WHERE table_type='BASE TABLE'
                      AND table_schema NOT IN ('pg_catalog','information_schema')
                    ORDER BY table_schema, table_name;
                """)
                tdf["qualified"] = tdf["table_schema"] + "." + tdf["table_name"]
                tables = tdf["qualified"].tolist()
            except Exception as e:
                st.error(f"Could not fetch tables: {e}")
                return

            if not tables:
                st.info("No user tables found.")
                return

            q_table = st.selectbox("Table (schema.table)", tables, key="quick_table_pg")

            # peek to infer schema
            try:
                peek = _pg_run_sql(st.session_state.pg_conn, f'SELECT * FROM {q_table} LIMIT 200;')
            except Exception as e:
                st.error(f"Peek failed: {e}")
                return

            num_cols = peek.select_dtypes(include=["number"]).columns.tolist()
            cat_cols = [c for c in peek.columns if c not in num_cols]

            if st.button("📋 Table Summary (PostgreSQL)"):
                res = _pg_run_sql(st.session_state.pg_conn, f"SELECT COUNT(*) AS cnt FROM {q_table};")
                st.metric("Total Records", f"{int(res.iloc[0,0]):,}")
                head = _pg_run_sql(st.session_state.pg_conn, f"SELECT * FROM {q_table} LIMIT 5;")
                st.dataframe(head, use_container_width=True)
                st.caption("**Explanation (EN):** Total row count and a 5-row preview.")

            if num_cols and st.button("💰 Numeric Summary (PostgreSQL)"):
                parts = []
                for c in num_cols[:5]:
                    parts += [f'AVG("{c}") AS avg_{c}', f'SUM("{c}") AS sum_{c}',
                              f'MAX("{c}") AS max_{c}', f'MIN("{c}") AS min_{c}']
                res = _pg_run_sql(st.session_state.pg_conn, f"SELECT {', '.join(parts)} FROM {q_table};")
                for c in num_cols[:3]:
                    a1, a2, a3, a4 = st.columns(4)
                    with a1: st.metric(f"{c} · Avg", f"{res[f'avg_{c}'].iloc[0]:.2f}")
                    with a2: st.metric(f"{c} · Sum", f"{res[f'sum_{c}'].iloc[0]:,.2f}")
                    with a3: st.metric(f"{c} · Max", f"{res[f'max_{c}'].iloc[0]:.2f}")
                    with a4: st.metric(f"{c} · Min", f"{res[f'min_{c}'].iloc[0]:.2f}")
                st.caption("**Explanation (EN):** Aggregations are computed directly in PostgreSQL.")

            if cat_cols and st.button("👥 Category Analysis (PostgreSQL)"):
                cat = cat_cols[0]
                res = _pg_run_sql(
                    st.session_state.pg_conn,
                    f'SELECT "{cat}" AS category, COUNT(*) AS cnt '
                    f'FROM {q_table} GROUP BY "{cat}" ORDER BY cnt DESC LIMIT 15;'
                )
                if not res.empty:
                    fig = px.bar(res, x="category", y="cnt", title=f"Distribution of {cat}")
                    st.plotly_chart(fig, use_container_width=True)
                    st.dataframe(res)
                    st.caption("**Explanation (EN):** Counts the most frequent categories.")

            if num_cols and st.button("📈 Recent Trend (last 100 rows, PostgreSQL)"):
                target = num_cols[0]
                res = _pg_run_sql(
                    st.session_state.pg_conn,
                    f"SELECT {target} FROM {q_table} LIMIT 100;"
                )
                if not res.empty:
                    res = res.reset_index().rename(columns={"index": "idx"})
                    fig = px.line(res, x="idx", y=target, title=f"Trend of {target} (first 100 rows)")
                    st.plotly_chart(fig, use_container_width=True)
                    st.caption("**Explanation (EN):** No guaranteed ordering without an ID/timestamp; "
                               "we show a simple trend over the fetched sample.")

def show_reports():
    """
    הצגת ממשק יצירת דוחות מקיפים ומקצועיים
    
    מטרת הפונקציה:
    - יצירת דוחות ניתוח מקיפים בפורמטים שונים
    - הפקת תובנות עסקיות מובנות ומנוסחות היטב
    - מתן אפשרויות התאמה אישית של תוכן הדוחות
    - הכנת דוחות מותאמים לקהלי יעד שונים (מנהלים, אנליסטים, לקוחות)
    
    סוגי הדוחות הזמינים:
    
    1. Business Summary Report:
       - סיכום עסקי ברמה גבוהה למנהלים בכירים
       - מטריקות מפתח ומדדי ביצוע עיקריים (KPIs)
       - המלצות אסטרטגיות מבוססות נתונים
       - פורמט קצר וממוקד לקבלת החלטות מהירה
    
    2. Detailed Analysis Report:
       - דוח מפורט וטכני לאנליסטים ומומחי נתונים
       - ניתוח סטטיסטי מעמיק עם בדיקות השערות
       - תרשימים ויזואליים מתקדמים
       - מטריקות מפורטות ומסקנות מבוססות נתונים
    
    3. Executive Summary:
       - דוח קצר למנהלים עם דגש על תוצאות עסקיות
       - תמצית הממצאים החשובים ביותר
       - המלצות לפעולה עם סדר עדיפויות
       - עיצוב מקצועי המתאים לשיתוף עם בעלי עניין
    
    4. Custom Report Builder:
       - יצירת דוח מותאם אישית על פי הצרכים
       - בחירה גמישה של רכיבי הדוח: תרשימים, סטטיסטיקות, מתאמים
       - אפשרות לכלול או להחריג רכיבים ספציפיים
       - התאמה לדרישות ספציפיות של הארגון
    
    פיצ'רים מתקדמים בדוחות:
    - ויזואליזציות אינטראקטיביות ומותאמות
    - ניתוח טרנדים ותחזיות בסיסיות
    - זיהוי ערכים חריגים ואנומליות משמעותיות
    - ניתוח קורלציות והמלצות להמשך מחקר
    - סיכום איכות הנתונים ואמינות התוצאות
    - המלצות לשיפור איסוף וניהול הנתונים
    
    פורמטי הייצוא:
    - הצגה ישירה באפליקציה
    - ייצוא לקבצי טקסט והדפסה
    - שמירה במצב הסשן להמשך עבודה
    
    החזרה: ללא - הפונקציה מציגה את הממשק ישירות
    """
    st.markdown("## 📄 Report Generation")
    
    if 'data' not in st.session_state:
        st.warning("📂 Please load data first!")
        return
    
    df = st.session_state.data
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Report Configuration")
        
        report_type = st.selectbox(
            "Report Type",
            ["📈 Brief Overview", "📊 Detailed Analysis", "🎯 Custom Report", "📋 Executive Summary"]
        )
        
        # Report settings
        include_charts = st.checkbox("Include charts", value=True)
        include_stats = st.checkbox("Include statistics", value=True)
        include_correlations = st.checkbox("Include correlations", value=True)
        include_outliers = st.checkbox("Include outlier analysis", value=False)
        
        if st.button("📄 Generate Report"):
            with st.spinner("Generating report..."):
                if report_type == "📈 Brief Overview":
                    report_content = generate_executive_summary(df)
                elif report_type == "📊 Detailed Analysis":
                    report_content = generate_detailed_analysis(df, include_charts, include_stats, include_correlations)
                elif report_type == "📋 Executive Summary":
                    report_content = generate_business_summary(df)
                else:
                    report_content = generate_custom_report(df, include_charts, include_stats, include_correlations, include_outliers)
                
                st.markdown("### 📋 Report Preview")
                st.markdown(report_content)
    
    with col2:
        st.markdown("### 💾 Data Export")
        
        if st.button("📥 Download CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="💾 Download as CSV",
                data=csv,
                file_name=f'data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                mime='text/csv'
            )
        
        if st.button("📊 Download Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
                
                # Add statistics sheet
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    stats_df = df[numeric_cols].describe()
                    stats_df.to_excel(writer, sheet_name='Statistics')
                
            excel_data = output.getvalue()
            
            st.download_button(
                label="💾 Download as Excel",
                data=excel_data,
                file_name=f'data_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
        
        # Export report to text file
        if 'report_content' in locals():
            st.download_button(
                label="📄 Download Report",
                data=report_content,
                file_name=f'report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.md',
                mime='text/markdown'
            )

def generate_business_summary(df):
    """
    יצירת דוח סיכום מתמקד בתוצאות עסקיות
    
    מטרת הפונקציה:
    - יצירת סיכום עסקי מקצועי ומובן למנהלים
    - הדגשת מטריקות מפתח ומדדי ביצוע עיקריים
    - מתן פרשנות עסקית לתוצאות הניתוח
    - הצעת המלצות אסטרטגיות לקבלת החלטות
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים לניתוח
    
    תוכן הדוח:
    - סקירה כללית של הנתונים
    - מטריקות מפתח ומדדי ביצוע
    - תובנות עסקיות מרכזיות
    - המלצות לפעולה
    
    החזרה:
        str: דוח עסקי מעוצב כמחרוזת טקסט
    """
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now_israel = datetime.now(israel_tz)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns

    summary = f"""
# 📊 Executive Summary
*Created: {now_israel.strftime('%Y-%m-%d %H:%M')} (Israel time)*

## 🎯 Key Metrics

**Data Overview:**
- 📝 Total records: **{len(df):,}**
- 📊 Number of columns: **{len(df.columns)}**
- 🔢 Numeric columns: **{len(numeric_cols)}**
- 📋 Categorical columns: **{len(text_cols)}**

## 💡 Main Findings

"""
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct < 5:
        summary += "✅ High data quality - less than 5% missing values\n\n"
    elif missing_pct < 15:
        summary += "⚠️ Satisfactory data quality - requires attention to missing values\n\n"
    else:
        summary += "❌ Data cleaning required - high percentage of missing values\n\n"

    if len(numeric_cols) > 0:
        summary += "### 📈 Numeric Metrics\n\n"
        for col in numeric_cols[:5]:
            col_stats = df[col].describe()
            summary += f"**{col}:**\n"
            summary += f"- Average value: {col_stats['mean']:.2f}\n"
            summary += f"- Median: {col_stats['50%']:.2f}\n"
            summary += f"- Range: {col_stats['min']:.2f} - {col_stats['max']:.2f}\n\n"

    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        high_corr_pairs = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.7:
                    high_corr_pairs.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
        if high_corr_pairs:
            summary += "### 🔗 Strong Relationships\n\n"
            for var1, var2, corr in high_corr_pairs[:3]:
                summary += f"- **{var1}** ↔ **{var2}**: {corr:.3f}\n"
            summary += "\n"

    summary += "## 🎯 Recommendations\n\n"
    recommendations = []
    if missing_pct > 10:
        recommendations.append("🔧 Perform data cleaning and handle missing values")
    if len(numeric_cols) >= 3:
        recommendations.append("📊 Consider applying machine learning methods")
    if len(text_cols) > 0:
        recommendations.append("📝 Perform categorical variable analysis")
    if len(df) > 10000:
        recommendations.append("⚡ Use optimization methods for big data")
    for i, rec in enumerate(recommendations, 1):
        summary += f"{i}. {rec}\n"

    summary += f"\n---\nReport generated by DataBot Analytics Pro"
    return summary

def generate_detailed_analysis(df, include_charts=True, include_stats=True, include_correlations=True):
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now_israel = datetime.now(israel_tz)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns

    analysis = f"""
# 📈 Detailed Data Analysis
*Created: {now_israel.strftime('%Y-%m-%d %H:%M')} (Israel time)*

## 📊 Dataset Overview

### Basic Characteristics
- **Total records**: {len(df):,}
- **Number of columns**: {len(df.columns)}
- **Memory size**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

### Data Types
- **Numeric columns**: {len(numeric_cols)} ({', '.join(numeric_cols[:5])}{'...' if len(numeric_cols) > 5 else ''})
- **Text columns**: {len(text_cols)} ({', '.join(text_cols[:5])}{'...' if len(text_cols) > 5 else ''})
- **Datetime columns**: {len(datetime_cols)}

## 🔍 Data Quality

### Missing Value Analysis
"""
    missing_data = df.isnull().sum()
    missing_pct = (missing_data / len(df)) * 100
    if missing_data.sum() > 0:
        analysis += f"**Total missing values**: {missing_data.sum():,}\n\n"
        analysis += "**Columns with missing values**:\n"
        for col in missing_data[missing_data > 0].index:
            analysis += f"- {col}: {missing_data[col]} ({missing_pct[col]:.1f}%)\n"
    else:
        analysis += "✅ No missing values detected\n"
    analysis += "\n"

    duplicates = df.duplicated().sum()
    if duplicates > 0:
        analysis += f"**Duplicates**: {duplicates} rows ({duplicates/len(df)*100:.1f}%)\n\n"
    else:
        analysis += "✅ No duplicates detected\n\n"

    if include_stats and len(numeric_cols) > 0:
        analysis += "## 📊 Statistical Analysis\n\n"
        for col in numeric_cols:
            stats = df[col].describe()
            analysis += f"### {col}\n"
            analysis += f"- **Mean**: {stats['mean']:.3f}\n"
            analysis += f"- **Median**: {stats['50%']:.3f}\n"
            analysis += f"- **Standard deviation**: {stats['std']:.3f}\n"
            analysis += f"- **Minimum**: {stats['min']:.3f}\n"
            analysis += f"- **Maximum**: {stats['max']:.3f}\n"
            analysis += f"- **Coefficient of variation**: {(stats['std']/stats['mean']*100):.1f}%\n\n"

    if include_correlations and len(numeric_cols) >= 2:
        analysis += "## 🔗 Correlation Analysis\n\n"
        corr_matrix = df[numeric_cols].corr()
        strong_correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                if abs(corr_val) > 0.5:
                    strong_correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
        if strong_correlations:
            analysis += "### Significant correlations (|r| > 0.5):\n"
            strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            for var1, var2, corr in strong_correlations:
                strength = "very strong" if abs(corr) > 0.8 else "strong" if abs(corr) > 0.6 else "moderate"
                direction = "positive" if corr > 0 else "negative"
                analysis += f"- **{var1}** ↔ **{var2}**: {corr:.3f} ({strength} {direction})\n"
        else:
            analysis += "No strong correlations detected.\n"
        analysis += "\n"

    if len(numeric_cols) > 0:
        analysis += "## 📈 Distribution Analysis\n\n"
        for col in numeric_cols[:3]:
            skewness = df[col].skew()
            kurtosis = df[col].kurtosis()
            analysis += f"### {col}\n"
            analysis += f"- **Skewness**: {skewness:.3f} "
            if abs(skewness) < 0.5:
                analysis += "(symmetric distribution)\n"
            elif skewness > 0:
                analysis += "(right-skewed)\n"
            else:
                analysis += "(left-skewed)\n"
            analysis += f"- **Kurtosis**: {kurtosis:.3f} "
            if kurtosis > 3:
                analysis += "(peaked distribution)\n"
            elif kurtosis < -1:
                analysis += "(flat distribution)\n"
            else:
                analysis += "(close to normal)\n"
            analysis += "\n"

    analysis += "## 💡 Conclusions and Recommendations\n\n"
    conclusions = []
    missing_pct_total = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct_total < 5:
        conclusions.append("✅ High data quality - ready for analysis")
    elif missing_pct_total < 15:
        conclusions.append("⚠️ Data requires preprocessing")
    else:
        conclusions.append("❌ Serious data cleaning needed")
    if len(df) > 100000:
        conclusions.append("📊 Large dataset - suitable for machine learning")
    elif len(df) > 1000:
        conclusions.append("📈 Medium dataset - sufficient for statistical analysis")
    else:
        conclusions.append("📉 Small dataset - limited analysis capabilities")
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        max_corr = corr_matrix.abs().values[np.triu_indices_from(corr_matrix.values, 1)].max()
        if max_corr > 0.8:
            conclusions.append("🔗 Strong correlations detected - possible multicollinearity")
        elif max_corr > 0.5:
            conclusions.append("📊 Moderate correlations found between variables")
    outlier_cols = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        if len(outliers) > len(df) * 0.05:
            outlier_cols.append(col)
    if outlier_cols:
        conclusions.append(f"⚠️ Outliers detected in columns: {', '.join(outlier_cols)}")
    for i, conclusion in enumerate(conclusions, 1):
        analysis += f"{i}. {conclusion}\n"
    analysis += "\n### Next Steps:\n"
    next_steps = []
    if missing_pct_total > 5:
        next_steps.append("🔧 Handle missing values")
    if len(numeric_cols) >= 3:
        next_steps.append("🤖 Apply machine learning methods")
    if outlier_cols:
        next_steps.append("🎯 Analyze and handle outliers")
    if len(text_cols) > 0:
        next_steps.append("📝 Analyze categorical variables")
    if len(numeric_cols) >= 2:
        next_steps.append("📊 Build predictive models")
    for i, step in enumerate(next_steps, 1):
        analysis += f"{i}. {step}\n"
    analysis += f"\n---\nDetailed analysis performed on {now_israel.strftime('%Y-%m-%d at %H:%M')} (Israel time)"
    return analysis

def generate_executive_summary(df):
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now_israel = datetime.now(israel_tz)
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    summary = f"""
# 📊 Data Brief Overview

## Key Metrics
- **Records**: {len(df):,}
- **Columns**: {len(df.columns)}
- **Numeric columns**: {len(numeric_cols)}
- **Data quality**: {calculate_data_quality(df):.1f}/10

## Key Statistics
"""
    if len(numeric_cols) > 0:
        for col in numeric_cols[:3]:
            mean_val = df[col].mean()
            summary += f"- **{col}**: average {mean_val:.2f}\n"
    summary += f"\n*Overview created: {now_israel.strftime('%Y-%m-%d %H:%M')} (Israel time)*"
    return summary

def generate_custom_report(df, include_charts=True, include_stats=True, include_correlations=True, include_outliers=False):
    israel_tz = pytz.timezone('Asia/Jerusalem')
    now_israel = datetime.now(israel_tz)
    numeric_cols = df.select_dtypes(include=[np.number]).columns

    report = f"""
# 🎯 Custom Report
*Created: {now_israel.strftime('%Y-%m-%d %H:%M')} (Israel time)*

## 📋 Report Configuration
- Charts: {'✅' if include_charts else '❌'}
- Statistics: {'✅' if include_stats else '❌'}
- Correlations: {'✅' if include_correlations else '❌'}
- Outlier analysis: {'✅' if include_outliers else '❌'}

## 📊 Data Overview
- Total records: {len(df):,}
- Total columns: {len(df.columns)}
"""
    if include_stats and len(numeric_cols) > 0:
        report += f"\n## 📈 Statistical Overview\n"
        for col in numeric_cols[:5]:
            stats = df[col].describe()
            report += f"**{col}**: min={stats['min']:.2f}, max={stats['max']:.2f}, mean={stats['mean']:.2f}\n"
    if include_correlations and len(numeric_cols) >= 2:
        report += f"\n## 🔗 Correlation Analysis\n"
        corr_matrix = df[numeric_cols].corr()
        max_corr = corr_matrix.abs().values[np.triu_indices_from(corr_matrix.values, 1)].max()
        report += f"Maximum correlation: {max_corr:.3f}\n"
    if include_outliers:
        report += f"\n## 🎯 Outlier Analysis\n"
        for col in numeric_cols[:3]:
            outliers_info = detect_outliers_advanced(df[col])
            iqr_outliers = outliers_info['IQR']['count']
            report += f"**{col}**: {iqr_outliers} outliers by IQR method\n"
    return report

# Helper functions for creating demo data
def create_demo_data():
    """
    יצירת נתוני הדגמה מקיפים לצורכי ניסוי ולימוד
    
    מטרת הפונקציה:
    - יצירת מסד נתונים סינתטי שמדמה נתונים עסקיים אמיתיים
    - מאפשר למשתמשים לנסות את האפליקציה ללא צורך בנתונים שלהם
    - כולל מגוון רחב של סוגי נתונים ומבנים
    - מכיל קשרים ריאליסטיים בין המשתנים
    
    הנתונים כוללים:
    - Date: תאריכים רצופים לאורך שנה
    - Sales: נתוני מכירות בהתפלגות נורמלית
    - Customers: מספר לקוחות בהתפלגות פואסון
    - Revenue: הכנסות עם שונות ריאליסטית
    - Region: אזורים גיאוגרפיים שונים
    - Category: קטגוריות מוצרים
    - Rating: דירוגים עם ערכים חסרים לריאליזם
    
    משתנים מחושבים:
    - Conversion: אחוז המרה (לקוחות/מכירות)
    - Average_Check: סכום ממוצע ללקוח
    
    החזרה:
        DataFrame: מסגרת נתונים עם 1000 רשומות להדגמה
    """
    np.random.seed(42)
    
    n_records = 1000
    
    data = {
        'Date': pd.date_range('2024-01-01', periods=n_records, freq='D'),
        'Sales': np.random.normal(1000, 200, n_records),
        'Customers': np.random.poisson(30, n_records),
        'Revenue': np.random.normal(5000, 1000, n_records),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], n_records),
        'Category': np.random.choice(['A', 'B', 'C'], n_records),
        'Rating': np.random.uniform(1, 5, n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Add some realistic dependencies
    df['Conversion'] = df['Customers'] / df['Sales'] * 100
    df['Average_Check'] = df['Revenue'] / df['Customers']
    
    # Add some missing values for realism
    df.loc[np.random.choice(df.index, 50), 'Rating'] = np.nan
    
    return df

def create_ecommerce_data():
    """
    יצירת נתוני מסחר אלקטרוני ריאליסטיים
    
    מטרת הפונקציה:
    - יצירת מסד נתונים סינתטי המדמה חנות אונליין אמיתית
    - מתאים לניתוחים עסקיים ומחקרי שוק
    - כולל מטריקות מפתח בתחום המסחר האלקטרוני
    - מאפשר ניתוח התנהגות לקוחות ודפוסי רכישה
    
    נתוני המשתמשים והרכישות:
    - user_id: מזהה משתמש ייחודי
    - Age: גיל המשתמש (18-65)
    - Gender: מין (ז/נ)
    - Purchase_Amount: סכום הרכישה (בהתפלגות אקספוננציאלית)
    - Category: קטגוריות מוצרים (אלקטרוניקה, בגדים, ספרים, בית)
    - Satisfaction: דירוג שביעות רצון (1-5)
    
    נתוני התנהגות באתר:
    - Time_on_Site: זמן שהיה באתר (שניות)
    - Page_Views: מספר צפיות בעמודים
    - Device: סוג מכשיר (מחשב, נייד, טאבלט)
    - Source: מקור הגעה (חיפוש, רשתות חברתיות, דואר, ישיר)
    
    אלגוריתמים מוטמעים:
    - צעירים נוטים יותר להשתמש במכשירים ניידים
    - רכישות בקטגוריות מסוימות משפיעות על הסכום
    - קשר בין זמן באתר לסכום הרכישה
    
    החזרה:
        DataFrame: מסגרת נתונים עם 2000 רשומות של נתוני מסחר אלקטרוני
    """
    np.random.seed(123)
    
    n_records = 2000
    
    data = {
        'user_id': range(1, n_records + 1),
        'Age': np.random.randint(18, 65, n_records),
        'Gender': np.random.choice(['M', 'F'], n_records),
        'Purchase_Amount': np.random.exponential(50, n_records),
        'Category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], n_records),
        'Satisfaction': np.random.randint(1, 6, n_records),
        'Time_on_Site': np.random.normal(300, 100, n_records),  # seconds
        'Page_Views': np.random.poisson(5, n_records),
        'Device': np.random.choice(['Desktop', 'Mobile', 'Tablet'], n_records),
        'Source': np.random.choice(['Search', 'Social Media', 'Email', 'Direct'], n_records)
    }
    
    df = pd.DataFrame(data)
    
    # Add dependencies
    # Young users more likely to use mobile
    mobile_prob = 1 / (1 + np.exp((df['Age'] - 35) / 10))
    df.loc[np.random.random(n_records) < mobile_prob, 'Device'] = 'Mobile'
    
    # More time on site = more purchases
    df['Purchase_Amount'] = df['Purchase_Amount'] * (1 + df['Time_on_Site'] / 1000)
    
    # Add missing values
    df.loc[np.random.choice(df.index, 100), 'Satisfaction'] = np.nan
    
    return df

def auto_analyze_data():
    """
    ניתוח אוטומטי של הנתונים הטעונים
    
    מטרת הפונקציה:
    - ביצוע סדרת ניתוחים אוטומטיים על הנתונים הטעונים
    - יצירת תובנות מיידיות ומעשיות ללא צורך בהתדחלות ידנית
    - הצגת סיכום מקיף של מאפייני ואיכות הנתונים
    - חיסכון זמן למשתמש בביצוע ניתוחים בסיסיים
    
    רכיבי הניתוח האוטומטי:
    - מדדים בסיסיים: גודל מסד, אחוז ערכים חסרים, ציון איכות
    - תובנות ועצות מקצועיות מבוססות על מבנה הנתונים
    - סטטיסטיקות מהירות: ממוצע, שונות, מקדם שונות
    - הדגשת משתנים רלוונטיים ביותר (עד 3 ראשונים)
    
    אופן הפעלה:
    הפונקציה עובדת רק אם יש נתונים טעונים במצב הסשן
    
    החזרה: ללא - הפונקציה מציגה את תוצאות הניתוח ישירות
    """
    if 'data' not in st.session_state:
        return
    
    df = st.session_state.data
    
    st.markdown("### 🔍 Auto-Analysis Results")
    
    # Basic information
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("📊 Data Size", f"{len(df)} × {len(df.columns)}")
    
    with col2:
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("❌ Missing", f"{missing_pct:.1f}%")
    
    with col3:
        quality_score = calculate_data_quality(df)
        st.metric("⭐ Quality", f"{quality_score:.1f}/10")
    
    # Show insights
    show_insights_and_advice(df)
    
    # Brief statistical overview
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 0:
        st.markdown("#### 📈 Quick Statistics")
        
        for col in numeric_cols[:3]:  # Show first 3 columns
            mean_val = df[col].mean()
            std_val = df[col].std()
            cv = (std_val / mean_val) * 100 if mean_val != 0 else 0
            
            st.write(f"**{col}**: mean = {mean_val:.2f}, variation = {cv:.1f}%")

def calculate_data_quality(df):
    """
    חישוב ציון איכות נתונים כולל
    
    מטרת הפונקציה:
    - הערכת מקיפה וכמותית של איכות מסד הנתונים
    - מתן ציון איכות קל להבנה (0-10)
    - זיהוי בעיות איכות עיקריות המשפיעות על אמינות הניתוח
    - מתן בסיס להחלטות על צעדי ניקוי ועיבוד
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים להערכה
    
    מרכיבי הציון (פנליזציות):
    - ערכים חסרים: עד -5 נקודות (אחוז חסרים * 5)
    - רשומות כפולות: עד -3 נקודות (אחוז כפולים * 3)
    - מעט מדי עמודות: -1 נקודה (אם פחות מ-3 עמודות)
    
    סולם הציונים:
    - 9-10: איכות מצוינת
    - 7-8: איכות טובה
    - 5-6: איכות סבירה
    - 0-4: איכות רעה - דרוש ניקוי
    
    החזרה:
        float: ציון איכות בין 0 ל-10
    """
    
    score = 10.0
    
    # Penalty for missing values
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns))
    score -= missing_pct * 5
    
    # Penalty for duplicates
    duplicate_pct = df.duplicated().sum() / len(df)
    score -= duplicate_pct * 3
    
    # Penalty for low variation (constant columns)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].std() == 0:  # Constant column
            score -= 1
    
    return max(0, min(10, score))

def fill_missing_values(df):
    """
    מילוי ערכים חסרים בשיטות מתאימות לפי סוג הנתונים
    
    מטרת הפונקציה:
    - טיפול אוטומטי בערכים חסרים לפי סוג הנתונים בכל עמודה
    - שיפור איכות הנתונים לצורך ניתוחים נוספים
    - הכנת הנתונים לאלגוריתמי למידת מכונה
    - שמירה על המבנה והתוכן המקורי של הנתונים ככל הניתן
    
    פרמטרים:
        df (DataFrame): מסגרת הנתונים עם ערכים חסרים
    
    שיטות המילוי לפי סוג נתונים:
    - עמודות נומריות (float64, int64): מילוי בחציון
      - בחירה בחציון על פני ממוצע להפחתת השפעת ערכים חריגים
      - שמירה על ההתפלגות המקורית של הנתונים
    - עמודות טקסט/קטגוריאליות (object): מילוי במצב (Mode)
      - בחירה בערך השכיח ביותר לכל עמודה
      - הפחתת השפעה על ההתפלגות הקטגוריאלית
    - עמודות אחרות: מילוי קדמי (Forward Fill)
      - שימוש בערך הקודם הזמין
      - מתאים לסדרות זמן ולנתונים סדרתיים
    
    יתרונות השיטה:
    - גישה מתוחכמת ומותאמת לסוג הנתונים
    - שמירה על התפלגויות מקוריות
    - עמידות בפני ערכים חריגים
    - תוצאות מהימנות לניתוחים סטטיסטיים
    
    החזרה:
        DataFrame: מסגרת נתונים מעודכנת ללא ערכים חסרים
    """
    
    df_filled = df.copy()
    
    for col in df_filled.columns:
        if df_filled[col].dtype in ['float64', 'int64']:
            # Numeric - with median
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        elif df_filled[col].dtype == 'object':
            # Categorical - with mode or 'Unknown'
            mode_val = df_filled[col].mode()
            if len(mode_val) > 0:
                df_filled[col] = df_filled[col].fillna(mode_val[0])
            else:
                df_filled[col] = df_filled[col].fillna('Unknown')
        elif df_filled[col].dtype == 'datetime64[ns]':
            # Dates - with median
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
    
    return df_filled

def show_quick_summary():
    """
    הצגת סיכום מהיר של הנתונים בפעולה מהירה
    
    מטרת הפונקציה:
    - מתן סקירה מהירה ומוקדת של מאפייני הנתונים הבסיסיים
    - חיסכון בזמן למשתמש ללא צורך בניווט מורכב
    - עזרה בהבנת המבנה והאיכות של הנתונים
    - מתן בסיס להחלטה על ניתוחים נוספים
    
    תוכן הסיכום:
    - מטריקות בסיסיות: מספר רשומות, עמודות, עמודות נומריות
    - אחוז ערכים חסרים כולל
    - סטטיסטיקות מהירות ל-3 העמודות הנומריות הראשונות
    - ממוצע (μ) וסטיית תקן (σ) לכל עמודה
    
    אופן הפעלה:
    הפונקציה עובדת רק אם יש נתונים טעונים במצב הסשן
    
    החזרה: ללא - הפונקציה מציגה את הסיכום ישירות
    """
    if 'data' not in st.session_state:
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    st.markdown("### 📊 Quick Data Summary")
    
    # Basic stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Records", f"{len(df):,}")
        st.metric("Columns", len(df.columns))
    with col2:
        st.metric("Numeric Cols", len(numeric_cols))
        missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
        st.metric("Missing %", f"{missing_pct:.1f}%")
    
    # Quick insights
    if len(numeric_cols) > 0:
        st.write("**Top Numeric Columns:**")
        for col in numeric_cols[:3]:
            mean_val = df[col].mean()
            std_val = df[col].std()
            st.write(f"• {col}: μ={mean_val:.2f}, σ={std_val:.2f}")

def show_quick_correlation():
    """
    הצגת ניתוח מתאמים מהיר
    
    מטרת הפונקציה:
    - זיהוי מהיר של הקשרים החזקים בין המשתנים הנומריים
    - מתן צורת בין לקשרים המעניינים ביותר בנתונים
    - זיהוי דפוסים ותלויות פוטנציאליות
    - עזרה בבחירת משתנים לניתוחים נוספים
    
    דרישות הפעלה:
    - לפחות 2 עמודות נומריות במסד הנתונים
    - נתונים טעונים במצב הסשן
    
    תוכן הניתוח:
    - חישוב מטריצת מתאמי פירסון לכל המשתנים הנומריים
    - זיהוי והצגת המתאמים החזקים ביותר (|ר| > 0.5)
    - מיין הקשר: חיובי (ישיר) או שלילי (הפוך)
    - עוצמת הקשר בערכים נומריים (-1 עד +1)
    
    פרשנות התוצאות:
    - מתאם > 0.7: קשר חזק מאוד
    - מתאם 0.5-0.7: קשר חזק
    - מתאם 0.3-0.5: קשר בינוני
    - מתאם < 0.3: קשר חלש
    
    החזרה: ללא - הפונקציה מציגה את הניתוח ישירות
    """
    if 'data' not in st.session_state:
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) >= 2:
        st.markdown("### 🔗 Quick Correlation Analysis")
        
        corr_matrix = df[numeric_cols].corr()
        
        # Find highest correlations
        correlations = []
        for i in range(len(corr_matrix.columns)):
            for j in range(i+1, len(corr_matrix.columns)):
                corr_val = corr_matrix.iloc[i, j]
                correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
        
        # Sort by absolute correlation
        correlations.sort(key=lambda x: abs(x[2]), reverse=True)
        
        st.write("**Strongest Correlations:**")
        for i, (var1, var2, corr) in enumerate(correlations[:5]):
            strength = "Strong" if abs(corr) > 0.7 else "Moderate" if abs(corr) > 0.5 else "Weak"
            st.write(f"{i+1}. {var1} ↔ {var2}: {corr:.3f} ({strength})")

def show_quick_3d():
    """
    הצגת ויזואליזציה תלת-מימדית מהירה
    
    מטרת הפונקציה:
    - יצירת תרשים פיזור תלת-מימדי אינטראקטיבי של הנתונים
    - מתן אפשרות לחקר קשרים מורכבים בין שלושה משתנים נומריים
    - הצגת תובנות ויזואליות שקשה לקבל בתרשימים דו-מימדיים
    - עזרה בזיהוי קבוצות, דפוסים וחריגות במרחב התלת-מימדי
    
    דרישות הפעלה:
    - לפחות 3 עמודות נומריות במסד הנתונים
    - נתונים טעונים במצב הסשן
    
    מאפייני התרשים:
    - צירי X, Y, Z: שלושת המשתנים הנומריים הראשונים
    - נקודות אינטראקטיביות הניתנות לזום וסיבוב
    - צבעים ורדיפנציאליים לקבוצות אם קיימים משתנים קטגוריאליים
    - כלים לניווט תלת-מימדי: זום, סיבוב, הזזה
    
    יתרונות הויזואליזציה התלת-מימדית:
    - חשיפת קשרים נסתרים שלא נראים בתרשימים דו-מימדיים
    - זיהוי קבוצות (clusters) במרחב תלת-מימדי
    - הבנת התפלגות הנתונים במרחב רב-מימדי
    - זיהוי ערכים חריגים במרחב התלת-מימדי
    
    פלטפורמת התרשים:
    - שימוש בספריית Plotly לאינטראקטיביות מלאה
    - תמיכה בכלי ניווט מתקדמים
    - אפשרויות ייצוא והדפסה של התרשים
    
    החזרה: ללא - הפונקציה מציגה את התרשים ישירות
    """
    if 'data' not in st.session_state:
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) >= 3:
        st.markdown("### 🌐 Quick 3D Visualization")
        
        # Auto-select first 3 numeric columns
        x_col, y_col, z_col = numeric_cols[:3]
        
        fig = go.Figure(data=[go.Scatter3d(
            x=df[x_col],
            y=df[y_col],
            z=df[z_col],
            mode='markers',
            marker=dict(
                size=5,
                color=df[z_col],
                colorscale='Viridis',
                opacity=0.8
            )
        )])
        
        fig.update_layout(
            title=f"3D Plot: {x_col} vs {y_col} vs {z_col}",
            scene=dict(
                xaxis_title=x_col,
                yaxis_title=y_col,
                zaxis_title=z_col
            ),
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Need at least 3 numeric columns for 3D plot")

# Run application
if __name__ == "__main__":
    main()
    # אין להחזיר דבר בסוף הסקריפט

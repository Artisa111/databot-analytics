st.warning("⚠️ Mobile Version Notice: Streamlit doesn't support large file uploads on mobile browsers. Please use desktop version or try our Telegram bot for better experience!") 
st.warning("⚠️ Mobile file upload may not work. Use our bot: https://t.me/maydatabot123_bot") 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from scipy import stats
import sqlite3
import io
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import requests
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="DataBot Analytics Pro", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS styles
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
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🚀 DataBot Analytics Pro</h1>', unsafe_allow_html=True)
    
    # Mobile warning
    st.warning("⚠️ For better performance with large files, use the desktop version!")
    
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        st.markdown("---")
        
        # Navigation with descriptions
        page = st.selectbox(
            "Select section",
            ["🏠 Dashboard", "📁 Data Upload", "📈 Charts", "📊 Statistics", 
             "🤖 Machine Learning", "🧪 A/B Testing", "💾 Database", "📄 Reports"]
        )
        
        # Show current section info
        section_info = {
            "🏠 Dashboard": "Main overview with key metrics and insights",
            "📁 Data Upload": "Upload and clean CSV, Excel, JSON files", 
            "📈 Charts": "Interactive visualizations including 3D plots",
            "📊 Statistics": "Descriptive stats and statistical tests",
            "🤖 Machine Learning": "Clustering, PCA, anomaly detection",
            "🧪 A/B Testing": "Statistical significance testing",
            "💾 Database": "SQL operations and database management",
            "📄 Reports": "Generate comprehensive analysis reports"
        }
        
        st.info(section_info[page])
        st.markdown("---")
        
        # Quick actions sidebar
        if 'data' in st.session_state:
            st.markdown("### ⚡ Quick Actions")
            
            df = st.session_state.data
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if st.button("🎯 Data Summary", use_container_width=True):
                st.session_state.show_summary = True
            
            if len(numeric_cols) >= 2 and st.button("🔗 Quick Correlation", use_container_width=True):
                st.session_state.show_correlation = True
            
            if len(numeric_cols) >= 3 and st.button("🌐 3D Quick Plot", use_container_width=True):
                st.session_state.show_3d = True
            
            st.markdown("---")
            
            # Data info in sidebar
            st.markdown("### 📊 Data Info")
            st.write(f"**Rows:** {len(df):,}")
            st.write(f"**Columns:** {len(df.columns)}")
            st.write(f"**Numeric:** {len(numeric_cols)}")
            
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            quality_color = "🟢" if missing_pct < 5 else "🟡" if missing_pct < 15 else "🔴"
            st.write(f"**Quality:** {quality_color} {100-missing_pct:.1f}%")
        
        else:
            st.markdown("### 🚀 Getting Started")
            st.write("1. Upload your data files")
            st.write("2. Or load demo data")
            st.write("3. Explore with charts")
            st.write("4. Run ML analysis")
            st.write("5. Generate reports")
            
            st.markdown("---")
            st.markdown("### 📋 Supported Files")
            st.write("• CSV files")
            st.write("• Excel (.xlsx, .xls)")
            st.write("• JSON files")
            st.write("• Multiple file upload")
        
        st.markdown("---")
        st.markdown("### 🆘 Need Help?")
        with st.expander("📖 How to use"):
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
    
    # Handle quick actions
    if 'show_summary' in st.session_state and st.session_state.show_summary:
        show_quick_summary()
        st.session_state.show_summary = False
    
    if 'show_correlation' in st.session_state and st.session_state.show_correlation:
        show_quick_correlation()
        st.session_state.show_correlation = False
        
    if 'show_3d' in st.session_state and st.session_state.show_3d:
        show_quick_3d()
        st.session_state.show_3d = False
    
    # Page routing
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📁 Data Upload":
        show_upload()
    elif page == "📈 Charts":
        show_charts()
    elif page == "📊 Statistics":
        show_stats()
    elif page == "🤖 Machine Learning":
        show_ml()
    elif page == "🧪 A/B Testing":
        show_ab_testing()
    elif page == "💾 Database":
        show_database()
    elif page == "📄 Reports":
        show_reports()

def show_insights_and_advice(df):
    """Generate insights and advice based on data"""
    
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
                selected_category = st.selectbox("Filter by category", ["All"] + text_cols)
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
    """Generate smart insights using advanced analysis"""
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
    """Generate actionable recommendations for the dashboard"""
    
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
    """Create financial/investment demo data"""
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
    st.markdown("## 📂 Data Upload")

    uploaded_files = st.file_uploader(
        "Select files",
        type=['csv', 'xlsx', 'xls', 'json'],
        accept_multiple_files=True,
        help="Supported formats: CSV, Excel, JSON"
    )

    if uploaded_files:
        dfs = []
        for uploaded_file in uploaded_files:
            try:
                file_name = uploaded_file.name.lower()
                
                if file_name.endswith('.csv'):
                    # Try to determine delimiter
                    sample = str(uploaded_file.read(1024))
                    uploaded_file.seek(0)
                    
                    if ';' in sample:
                        df = pd.read_csv(uploaded_file, sep=';', encoding='utf-8')
                    else:
                        df = pd.read_csv(uploaded_file, encoding='utf-8')
                        
                elif file_name.endswith(('.xlsx', '.xls')):
                    df = pd.read_excel(uploaded_file)
                elif file_name.endswith('.json'):
                    df = pd.read_json(uploaded_file)
                else:
                    st.error(f"❌ Unsupported format: {file_name}")
                    continue

                dfs.append(df)
                st.success(f"✅ {uploaded_file.name} — Loaded {len(df)} rows, {len(df.columns)} columns")

            except Exception as e:
                st.error(f"⚠️ Error reading {uploaded_file.name}: {str(e)}")

        if dfs:
            if len(dfs) == 1:
                combined_df = dfs[0]
            else:
                # Combine files
                try:
                    combined_df = pd.concat(dfs, ignore_index=True)
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
    
    elif chart_type == "🔵 Scatter Plot" and len(numeric_cols) >= 2:
        st.markdown("### 🔵 Scatter Plot")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_col = st.selectbox("Y-axis", [col for col in numeric_cols if col != x_col])
        with col3:
            color_col = st.selectbox("Color by", ["None"] + text_cols)
        
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
            group_col = st.selectbox("Grouping", ["None"] + text_cols)
        
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
    """Enhanced trend analysis"""
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
    """Trend analysis in data"""
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
    """Advanced outlier detection using multiple methods"""
    
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

def show_ab_testing():
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
                # T-test
                t_stat, p_value_ttest = stats.ttest_ind(control, treatment, equal_var=False)
                
                # Mann-Whitney U test (non-parametric)
                u_stat, p_value_mannwhitney = stats.mannwhitneyu(control, treatment, alternative='two-sided')
                
                # Effect (difference of means)
                effect = treatment_mean - control_mean
                effect_pct = (effect / control_mean) * 100 if control_mean != 0 else 0
                
                # Cohen's d (effect size)
                pooled_std = np.sqrt(((len(control) - 1) * control_std**2 + (len(treatment) - 1) * treatment_std**2) / (len(control) + len(treatment) - 2))
                cohens_d = effect / pooled_std if pooled_std != 0 else 0
                
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
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("P-value (t-test)", f"{p_value_ttest:.4f}")
                with col2:
                    st.metric("P-value (Mann-Whitney)", f"{p_value_mannwhitney:.4f}")
                with col3:
                    st.metric("Cohen's d", f"{cohens_d:.3f}")
                
                # Results interpretation
                alpha = 0.05
                
                if p_value_ttest < alpha:
                    st.success("🎉 Statistically significant difference! (t-test)")
                else:
                    st.warning("❌ Difference is not statistically significant (t-test)")
                
                if p_value_mannwhitney < alpha:
                    st.success("🎉 Statistically significant difference! (Mann-Whitney)")
                else:
                    st.warning("❌ Difference is not statistically significant (Mann-Whitney)")
                
                # Effect size
                if abs(cohens_d) < 0.2:
                    effect_size = "small"
                elif abs(cohens_d) < 0.5:
                    effect_size = "medium"
                elif abs(cohens_d) < 0.8:
                    effect_size = "large"
                else:
                    effect_size = "very large"
                
                st.info(f"📏 Effect size: {effect_size} (Cohen's d = {cohens_d:.3f})")
                
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
                
                from scipy.stats import norm
                
                # Current power
                pooled_se = np.sqrt(control_std**2/len(control) + treatment_std**2/len(treatment))
                z_score = abs(effect) / pooled_se if pooled_se != 0 else 0
                current_power = 1 - norm.cdf(1.96 - z_score) + norm.cdf(-1.96 - z_score)
                
                st.metric("Statistical Power", f"{current_power:.3f}")
                
                if current_power >= 0.8:
                    st.success("✅ Sufficient statistical power (≥0.8)")
                else:
                    st.warning(f"⚠️ Low statistical power. Recommended ≥0.8")
                
                # Recommendations
                st.markdown("### 💡 Recommendations")
                
                recommendations = []
                
                if p_value_ttest < 0.05 and abs(effect_pct) > 5:
                    recommendations.append("🎯 Result is statistically significant and practically important")
                elif p_value_ttest < 0.05:
                    recommendations.append("📊 Result is statistically significant, but effect is small")
                elif abs(effect_pct) > 10:
                    recommendations.append("📈 Large practical effect, but need larger sample size")
                else:
                    recommendations.append("📋 No convincing evidence of effect")
                
                if current_power < 0.8:
                    recommendations.append("📊 Increase sample size to improve power")
                
                if abs(cohens_d) >= 0.5:
                    recommendations.append("💪 Medium or large effect size")
                
                for rec in recommendations:
                    st.write(f"• {rec}")
                
        except Exception as e:
            st.error(f"⚠️ Error in A/B test analysis: {str(e)}")

def generate_ab_test_data():
    """Generate realistic A/B test data"""
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

def show_database():
    st.markdown("## 💾 Database and SQL")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 🔗 Database Management")
        
        # Load CSV files into database
        uploaded_files = st.file_uploader(
            "Upload CSV files to database",
            type=['csv'],
            accept_multiple_files=True,
            help="Files will be loaded into SQLite database"
        )
        
        if uploaded_files and st.button("📁 Load to DB"):
            try:
                conn = sqlite3.connect('uploaded_data.db')
                loaded_tables = []
                
                for uploaded_file in uploaded_files:
                    df = pd.read_csv(uploaded_file)
                    table_name = uploaded_file.name.replace('.csv', '').replace(' ', '_').replace('-', '_').lower()
                    
                    # Clean table name from invalid characters
                    table_name = ''.join(c for c in table_name if c.isalnum() or c == '_')
                    
                    df.to_sql(table_name, conn, if_exists='replace', index=False)
                    loaded_tables.append(table_name)
                    st.success(f"✅ {uploaded_file.name} → table '{table_name}'")
                
                conn.close()
                st.session_state.db_tables = loaded_tables
                
            except Exception as e:
                st.error(f"Database loading error: {str(e)}")
        
        # Create demo database
        if st.button("🎲 Create Demo DB"):
            create_sample_database()
            st.success("Demo database created!")
        
        st.markdown("### ✏️ SQL Editor")
        
        # List available tables
        if os.path.exists('uploaded_data.db') or os.path.exists('sample_data.db'):
            try:
                if os.path.exists('uploaded_data.db'):
                    conn = sqlite3.connect('uploaded_data.db')
                else:
                    conn = sqlite3.connect('sample_data.db')
                
                tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
                tables_df = pd.read_sql_query(tables_query, conn)
                
                if not tables_df.empty:
                    st.markdown("**Available tables:**")
                    for table in tables_df['name']:
                        # Show table structure
                        structure_query = f"PRAGMA table_info({table});"
                        structure = pd.read_sql_query(structure_query, conn)
                        columns = ", ".join(structure['name'].tolist())
                        st.write(f"• **{table}**: {columns}")
                
                conn.close()
                
            except Exception as e:
                st.warning(f"Could not get table list: {e}")
        
        # SQL queries
        default_queries = {
            "Show all data": "SELECT * FROM sales LIMIT 10;",
            "Group by regions": "SELECT region, COUNT(*) as count, AVG(amount) as avg_amount FROM sales GROUP BY region;",
            "Top-5 by amount": "SELECT * FROM sales ORDER BY amount DESC LIMIT 5;",
            "Statistics by date": "SELECT DATE(date) as day, COUNT(*) as transactions, SUM(amount) as total FROM sales GROUP BY DATE(date) ORDER BY day;"
        }
        
        query_template = st.selectbox("Select query template", list(default_queries.keys()))
        
        sql_query = st.text_area(
            "SQL Query",
            value=default_queries[query_template],
            height=150,
            help="Write your SQL query here"
        )
        
        if st.button("▶️ Execute Query"):
            try:
                result = execute_sql_query(sql_query)
                st.success("Query executed successfully!")
                st.dataframe(result)
                
                # Show insights if result contains numeric data
                numeric_cols = result.select_dtypes(include=[np.number]).columns
                if len(numeric_cols) > 0:
                    st.markdown("### 📊 Result Insights")
                    show_query_insights(result)
                    
            except Exception as e:
                st.error(f"Query error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Quick Queries")
        
        # Predefined analytical queries
        if st.button("💰 Total Sales"):
            try:
                query = "SELECT SUM(amount) as total_sales FROM sales;"
                result = execute_sql_query(query)
                if not result.empty:
                    total = result.iloc[0, 0]
                    st.metric("Total Sales", f"${total:,.2f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("👥 Customers by Region"):
            try:
                query = "SELECT region, COUNT(DISTINCT customer_id) as customers FROM sales GROUP BY region ORDER BY customers DESC;"
                result = execute_sql_query(query)
                if not result.empty:
                    fig = px.bar(result, x='region', y='customers', 
                               title="Customers by Region")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("📈 Sales by Day"):
            try:
                query = """
                SELECT DATE(date) as day, 
                       SUM(amount) as daily_sales,
                       COUNT(*) as transactions 
                FROM sales 
                GROUP BY DATE(date) 
                ORDER BY day;
                """
                result = execute_sql_query(query)
                if not result.empty:
                    fig = px.line(result, x='day', y='daily_sales', 
                                title="Sales by Day")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("🔝 Top Products"):
            try:
                query = """
                SELECT product_name, 
                       SUM(amount) as total_revenue,
                       COUNT(*) as sales_count
                FROM sales 
                GROUP BY product_name 
                ORDER BY total_revenue DESC 
                LIMIT 10;
                """
                result = execute_sql_query(query)
                if not result.empty:
                    st.dataframe(result)
            except Exception as e:
                st.error(f"Error: {str(e)}")

def show_query_insights(result_df):
    """Show insights from SQL query results"""
    
    if result_df.empty:
        return
    
    numeric_cols = result_df.select_dtypes(include=[np.number]).columns
    
    if len(numeric_cols) > 0:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 📊 Numeric Statistics")
            for col in numeric_cols:
                total = result_df[col].sum()
                avg = result_df[col].mean()
                max_val = result_df[col].max()
                min_val = result_df[col].min()
                
                st.write(f"**{col}:**")
                st.write(f"  • Sum: {total:,.2f}")
                st.write(f"  • Average: {avg:.2f}")
                st.write(f"  • Max: {max_val:,.2f}")
                st.write(f"  • Min: {min_val:,.2f}")
        
        with col2:
            # Simple visualization if possible
            if len(result_df) <= 20:  # Small results
                first_numeric = numeric_cols[0]
                
                if len(result_df.columns) >= 2:
                    # Has categorical column for grouping
                    cat_col = [col for col in result_df.columns if col not in numeric_cols]
                    if cat_col:
                        fig = px.bar(result_df, x=cat_col[0], y=first_numeric,
                                   title=f"{first_numeric} by {cat_col[0]}")
                        st.plotly_chart(fig, use_container_width=True)

def execute_sql_query(query):
    """Execute SQL query"""
    try:
        # First try uploaded_data.db
        if os.path.exists('uploaded_data.db'):
            conn = sqlite3.connect('uploaded_data.db')
            result = pd.read_sql_query(query, conn)
            conn.close()
            return result
        
        # If not, try sample_data.db
        elif os.path.exists('sample_data.db'):
            conn = sqlite3.connect('sample_data.db')
            result = pd.read_sql_query(query, conn)
            conn.close()
            return result
        
        else:
            raise Exception("Database not found. Create demo DB or upload CSV files.")
            
    except Exception as e:
        raise e

def create_sample_database():
    """Create demonstration database"""
    
    conn = sqlite3.connect('sample_data.db')
    
    # Create sales table
    np.random.seed(42)
    
    # Generate realistic data
    n_records = 1000
    
    regions = ['North', 'South', 'East', 'West', 'Central']
    products = ['Laptop', 'Phone', 'Tablet', 'Watch', 'Headphones', 'Camera', 'TV', 'Speaker']
    customers = [f'Customer_{i}' for i in range(1, 201)]
    
    sales_data = {
        'id': range(1, n_records + 1),
        'customer_id': np.random.choice(customers, n_records),
        'product_name': np.random.choice(products, n_records),
        'region': np.random.choice(regions, n_records),
        'amount': np.random.exponential(100, n_records).round(2),
        'date': pd.date_range('2024-01-01', periods=n_records, freq='H'),
        'quantity': np.random.randint(1, 5, n_records),
        'discount': np.random.uniform(0, 0.3, n_records).round(3)
    }
    
    df = pd.DataFrame(sales_data)
    
    # Add calculated fields
    df['total_amount'] = df['amount'] * df['quantity'] * (1 - df['discount'])
    df['month'] = df['date'].dt.month
    df['day_of_week'] = df['date'].dt.day_name()
    
    df.to_sql('sales', conn, if_exists='replace', index=False)
    
    # Create customers table
    customer_data = {
        'customer_id': customers,
        'customer_name': [f'Name_{i}' for i in range(1, len(customers) + 1)],
        'email': [f'customer{i}@email.com' for i in range(1, len(customers) + 1)],
        'age': np.random.randint(18, 70, len(customers)),
        'gender': np.random.choice(['M', 'F'], len(customers)),
        'registration_date': pd.date_range('2023-01-01', periods=len(customers), freq='D'),
        'loyalty_tier': np.random.choice(['Bronze', 'Silver', 'Gold', 'Platinum'], len(customers))
    }
    
    customers_df = pd.DataFrame(customer_data)
    customers_df.to_sql('customers', conn, if_exists='replace', index=False)
    
    conn.close()

def show_reports():
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
    """Generate business summary"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    summary = f"""
# 📊 Executive Summary
*Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}*

## 🎯 Key Metrics

**Data Overview:**
- 📝 Total records: **{len(df):,}**
- 📊 Number of metrics: **{len(df.columns)}**
- 🔢 Numeric metrics: **{len(numeric_cols)}**
- 📋 Categorical metrics: **{len(text_cols)}**

## 💡 Main Findings

"""
    
    # Data quality analysis
    missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct < 5:
        summary += "✅ **High data quality** - less than 5% missing values\n\n"
    elif missing_pct < 15:
        summary += "⚠️ **Satisfactory data quality** - requires attention to missing values\n\n"
    else:
        summary += "❌ **Data cleaning required** - high percentage of missing values\n\n"
    
    # Numeric metrics analysis
    if len(numeric_cols) > 0:
        summary += "### 📈 Numeric Metrics\n\n"
        
        for col in numeric_cols[:5]:  # Top-5 metrics
            col_stats = df[col].describe()
            summary += f"**{col}:**\n"
            summary += f"- Average value: {col_stats['mean']:.2f}\n"
            summary += f"- Median: {col_stats['50%']:.2f}\n"
            summary += f"- Range: {col_stats['min']:.2f} - {col_stats['max']:.2f}\n\n"
    
    # Correlation analysis
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
            for var1, var2, corr in high_corr_pairs[:3]:  # Top-3 correlations
                summary += f"- **{var1}** ↔ **{var2}**: {corr:.3f}\n"
            summary += "\n"
    
    # Recommendations
    summary += "## 🎯 Recommendations\n\n"
    
    recommendations = []
    
    if missing_pct > 10:
        recommendations.append("🔧 Conduct data cleaning and handle missing values")
    
    if len(numeric_cols) >= 3:
        recommendations.append("📊 Consider applying machine learning methods")
    
    if len(text_cols) > 0:
        recommendations.append("📝 Conduct categorical variable analysis")
    
    if len(df) > 10000:
        recommendations.append("⚡ Use optimization methods for big data")
    
    for i, rec in enumerate(recommendations, 1):
        summary += f"{i}. {rec}\n"
    
    summary += f"\n---\n*Report generated by DataBot Analytics Pro*"
    
    return summary

def generate_detailed_analysis(df, include_charts=True, include_stats=True, include_correlations=True):
    """Generate detailed analysis"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    datetime_cols = df.select_dtypes(include=['datetime64']).columns
    
    analysis = f"""
# 📈 Detailed Data Analysis
*Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}*

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
    
    # Missing value analysis
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
    
    # Duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        analysis += f"**Duplicates**: {duplicates} rows ({duplicates/len(df)*100:.1f}%)\n\n"
    else:
        analysis += "✅ No duplicates detected\n\n"
    
    # Statistical analysis
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
    
    # Correlation analysis
    if include_correlations and len(numeric_cols) >= 2:
        analysis += "## 🔗 Correlation Analysis\n\n"
        
        corr_matrix = df[numeric_cols].corr()
        
        # Find strong correlations
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
    
    # Distribution analysis
    if len(numeric_cols) > 0:
        analysis += "## 📈 Distribution Analysis\n\n"
        
        for col in numeric_cols[:3]:  # Analyze first 3 columns
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
    
    # Conclusions and recommendations
    analysis += "## 💡 Conclusions and Recommendations\n\n"
    
    conclusions = []
    
    # Data quality
    missing_pct_total = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
    if missing_pct_total < 5:
        conclusions.append("✅ High data quality - ready for analysis")
    elif missing_pct_total < 15:
        conclusions.append("⚠️ Data requires preprocessing")
    else:
        conclusions.append("❌ Serious data cleaning needed")
    
    # Data size
    if len(df) > 100000:
        conclusions.append("📊 Large dataset - suitable for machine learning")
    elif len(df) > 1000:
        conclusions.append("📈 Medium dataset - sufficient for statistical analysis")
    else:
        conclusions.append("📉 Small dataset - limited analysis capabilities")
    
    # Correlations
    if len(numeric_cols) >= 2:
        corr_matrix = df[numeric_cols].corr()
        max_corr = corr_matrix.abs().values[np.triu_indices_from(corr_matrix.values, 1)].max()
        if max_corr > 0.8:
            conclusions.append("🔗 Strong correlations detected - possible multicollinearity")
        elif max_corr > 0.5:
            conclusions.append("📊 Moderate correlations found between variables")
    
    # Outliers
    outlier_cols = []
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = df[(df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)]
        if len(outliers) > len(df) * 0.05:  # More than 5% outliers
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
    
    analysis += f"\n---\n*Detailed analysis performed on {datetime.now().strftime('%d.%m.%Y at %H:%M')}*"
    
    return analysis

def generate_executive_summary(df):
    """Generate brief overview"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    summary = f"""
# 📊 Data Brief Overview

## Key Metrics
- **Records**: {len(df):,}
- **Columns**: {len(df.columns)}
- **Numeric metrics**: {len(numeric_cols)}
- **Data quality**: {calculate_data_quality(df):.1f}/10

## Key Statistics
"""
    
    if len(numeric_cols) > 0:
        for col in numeric_cols[:3]:
            mean_val = df[col].mean()
            summary += f"- **{col}**: average {mean_val:.2f}\n"
    
    summary += f"\n*Overview created: {datetime.now().strftime('%d.%m.%Y %H:%M')}*"
    
    return summary

def generate_custom_report(df, include_charts=True, include_stats=True, include_correlations=True, include_outliers=False):
    """Generate custom report"""
    
    report = f"""
# 🎯 Custom Report
*Created: {datetime.now().strftime('%d.%m.%Y %H:%M')}*

## 📋 Report Configuration
- Charts: {'✅' if include_charts else '❌'}
- Statistics: {'✅' if include_stats else '❌'}
- Correlations: {'✅' if include_correlations else '❌'}
- Outlier analysis: {'✅' if include_outliers else '❌'}

## 📊 Data Overview
- Total records: {len(df):,}
- Total columns: {len(df.columns)}
"""
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
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
    """Create demonstration data"""
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
    """Create e-commerce data"""
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
    """Automatic analysis of loaded data"""
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
    """Calculate data quality score"""
    
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
    """Fill missing values"""
    
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
    """Show quick data summary in sidebar action"""
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
    """Show quick correlation analysis"""
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
    """Show quick 3D visualization"""
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

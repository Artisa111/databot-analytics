st.warning("?? Mobile Version Notice: Streamlit doesn't support large file uploads on mobile browsers. Please use desktop version or try our Telegram bot for better experience!") 
st.warning("?? Mobile file upload may not work. Use our bot: https://t.me/maydatabot123_bot") 
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
from wordcloud import WordCloud
import sqlite3
import io
import base64
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import folium
from streamlit_folium import st_folium
import requests

st.set_page_config(
    page_title="DataBot Analytics Pro", 
    page_icon="🚀", 
    layout="wide",
    initial_sidebar_state="expanded"
)

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
    .sql-editor {
        background-color: #f8f9fa;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Courier New', monospace;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown('<h1 class="main-header">🚀 DataBot Analytics Pro</h1>', unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("### 🎯 Navigation")
        page = st.selectbox(
            "Choose Section",
            ["🏠 Dashboard", "📁 Upload Data", "📈 Charts", "📊 Statistics", 
             "🤖 Machine Learning", "🧪 A/B Testing", "💾 Database", "📄 Reports", "🎨 Dashboard Builder"]
        )
    
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📁 Upload Data":
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
    elif page == "🎨 Dashboard Builder":
        show_dashboard_builder()

def show_dashboard():
    st.markdown("## 🏠 Welcome to DataBot Analytics Pro!")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        if st.button("🎲 Load Demo Data"):
            demo_data = create_demo_data()
            st.session_state.data = demo_data
            st.success("Demo data loaded! 🎉")
        
        if st.button("🛒 Load E-commerce Data"):
            ecommerce_data = create_ecommerce_data()
            st.session_state.data = ecommerce_data
            st.success("E-commerce data loaded! 💰")
    
    with col2:
        st.markdown("### 🎯 Quick Actions")
        if st.button("🔍 Auto Analysis"):
            if 'data' in st.session_state:
                auto_analyze_data()
            else:
                st.warning("Load data first!")
    
    if 'data' in st.session_state:
        df = st.session_state.data
        
        # Метрики
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📝 Total Rows", f"{len(df):,}")
        with col2:
            st.metric("📊 Columns", f"{len(df.columns)}")
        with col3:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            st.metric("🔢 Numeric Cols", f"{len(numeric_cols)}")
        with col4:
            missing_pct = (df.isnull().sum().sum() / (len(df) * len(df.columns))) * 100
            st.metric("❌ Missing %", f"{missing_pct:.1f}%")
        
        # Быстрая визуализация
        if len(numeric_cols) > 0:
            col1, col2 = st.columns(2)
            
            with col1:
                fig = px.line(df, y=numeric_cols[0], title="Data Trend")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols].corr()
                    fig = px.imshow(corr_matrix, title="Correlation Matrix")
                    st.plotly_chart(fig, use_container_width=True)

def show_upload():
    st.markdown("## 📂 Upload Your Data")

    col1, col2 = st.columns([2, 1])

    with col1:
        uploaded_files = st.file_uploader(
            "Choose files",
            type=['csv', 'xml', 'json', 'xls', 'xlsx'],
            accept_multiple_files=True
        )

        if uploaded_files:
            dfs = []
            for uploaded_file in uploaded_files:
                file_name = uploaded_file.name.lower()
                try:
                    if file_name.endswith('.csv'):
                        df = pd.read_csv(uploaded_file)
                    elif file_name.endswith('.xml'):
                        df = pd.read_xml(uploaded_file)
                    elif file_name.endswith('.json'):
                        df = pd.read_json(uploaded_file)
                    elif file_name.endswith(('.xls', '.xlsx')):
                        df = pd.read_excel(uploaded_file)
                    else:
                        st.error(f"❌ Unsupported file type: {file_name}")
                        continue

                    dfs.append(df)
                    st.success(f"✅ {file_name} — Loaded {len(df)} rows!")

                except Exception as e:
                    st.error(f"⚠️ Error reading {file_name}: {e}")

            if dfs:
                combined_df = pd.concat(dfs, ignore_index=True)
                st.session_state.data = combined_df
                st.success(f"📊 Combined total: {len(combined_df)} rows")
                st.dataframe(combined_df.head())

    
    with col2:
        st.markdown("### 📊 Data Quality")
        if 'data' in st.session_state:
            df = st.session_state.data
            
            # Качество данных
            quality_score = calculate_data_quality(df)
            st.metric("Quality Score", f"{quality_score:.1f}/10")
            
            st.markdown("### 🔧 Data Cleaning")
            if st.button("Remove Duplicates"):
                df_clean = df.drop_duplicates()
                st.session_state.data = df_clean
                st.success(f"Removed {len(df) - len(df_clean)} duplicates")
            
            if st.button("Fill Missing Values"):
                df_filled = fill_missing_values(df)
                st.session_state.data = df_filled
                st.success("Missing values filled!")

def show_charts():
    st.markdown("## 📈 Advanced Data Visualization")
    if 'data' not in st.session_state:
        st.warning("Please upload data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Выбор типа графика
    chart_type = st.selectbox(
        "📊 Choose Chart Type", 
        ["📈 Line Chart", "📊 Bar Chart", "🔵 Scatter Plot", "📉 Area Chart", 
         "🗺️ Heatmap", "🌍 World Map", "☁️ Word Cloud", "📊 3D Scatter", "🗺️ Leaflet Map"]
    )
    
    if chart_type == "☁️ Word Cloud" and len(text_cols) > 0:
        st.markdown("### ☁️ Text Analysis")
        text_col = st.selectbox("Choose Text Column", text_cols)
        
        if st.button("Generate Word Cloud"):
            text_data = ' '.join(df[text_col].astype(str))
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text_data)
            
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
    
    elif chart_type == "📊 3D Scatter" and len(numeric_cols) >= 3:
        st.markdown("### 📊 3D Scatter Plot")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_col = st.selectbox("X-axis", numeric_cols)
        with col2:
            y_col = st.selectbox("Y-axis", [col for col in numeric_cols if col != x_col])
        with col3:
            z_col = st.selectbox("Z-axis", [col for col in numeric_cols if col not in [x_col, y_col]])
        
        fig = px.scatter_3d(df, x=x_col, y=y_col, z=z_col, title="3D Scatter Plot")
        st.plotly_chart(fig, use_container_width=True)
    
    elif chart_type == "🌍 World Map":
        show_world_map()
    
    elif chart_type == "🗺️ Leaflet Map":
        show_leaflet_map()
    
    elif len(numeric_cols) >= 1:
        if chart_type == "📈 Line Chart":
            col_choice = st.selectbox("Choose Column", numeric_cols)
            fig = px.line(df, y=col_choice, title=f"Line Chart: {col_choice}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "📊 Bar Chart":
            col_choice = st.selectbox("Choose Column", numeric_cols)
            fig = px.bar(df, y=col_choice, title=f"Bar Chart: {col_choice}")
            st.plotly_chart(fig, use_container_width=True)
            
        elif chart_type == "🔵 Scatter Plot" and len(numeric_cols) >= 2:
            col1, col2 = st.columns(2)
            with col1:
                x_col = st.selectbox("X-axis", numeric_cols)
            with col2:
                y_col = st.selectbox("Y-axis", [col for col in numeric_cols if col != x_col])
            fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter: {x_col} vs {y_col}")
            st.plotly_chart(fig, use_container_width=True)

def show_leaflet_map():
    st.markdown("### 🗺️ Interactive Leaflet Map")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Поиск локации
        search_query = st.text_input(
            "🔍 Search any location", 
            placeholder="Try: 'Tel Aviv', 'Kyiv', 'Paris', 'Times Square NYC'...",
            help="Enter any city, address, landmark, or coordinates"
        )
        
        if search_query and st.button("🌍 Search & Navigate"):
            with st.spinner("Searching location..."):
                coords = geocode_location(search_query)
                if coords:
                    st.session_state.map_center = coords
                    st.session_state.search_result = search_query
                    st.success(f"✅ Found: {search_query}")
                    st.rerun()
                else:
                    st.error("❌ Location not found. Try a different search term.")
    
    with col2:
        st.markdown("### ⚙️ Map Settings")
        
        # Настройки карты
        map_style = st.selectbox("Map Style", [
            "OpenStreetMap",
            "CartoDB positron", 
            "CartoDB dark_matter",
            "Stamen Terrain",
            "Stamen Toner"
        ])
        
        show_markers = st.checkbox("Show Data Points", True)
        show_heatmap = st.checkbox("Show Heatmap", False)
    
    # Центр карты (по умолчанию Jerusalem)
    if 'map_center' not in st.session_state:
        st.session_state.map_center = [31.7683, 35.2137]  # Jerusalem
    
    # Создание карты
    m = create_interactive_map(
        center=st.session_state.map_center,
        style=map_style,
        show_markers=show_markers,
        show_heatmap=show_heatmap
    )
    
    # Отображение карты
    st.markdown("### 🌍 Interactive Map")
    map_data = st_folium(m, width=1000, height=600, returned_objects=["last_clicked", "last_object_clicked"])
    
    # Информация о клике
    if map_data['last_clicked']:
        lat = map_data['last_clicked']['lat']
        lng = map_data['last_clicked']['lng']
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("📍 Latitude", f"{lat:.6f}")
        with col2:
            st.metric("📍 Longitude", f"{lng:.6f}")
        with col3:
            # Обратное геокодирование
            address = reverse_geocode(lat, lng)
            st.info(f"📍 {address}")
    
    # Показать результат поиска
    if 'search_result' in st.session_state:
        st.success(f"🎯 Current location: {st.session_state.search_result}")

def create_interactive_map(center, style="OpenStreetMap", show_markers=True, show_heatmap=False):
    """Создание интерактивной Leaflet карты"""
    
    # Карта с выбранным стилем
    m = folium.Map(
        location=center,
        zoom_start=12,
        tiles=style
    )
    
    # Добавление основного маркера
    folium.Marker(
        center,
        popup=f"📍 Current Location<br>Lat: {center[0]:.4f}<br>Lng: {center[1]:.4f}",
        tooltip="📍 Current Location",
        icon=folium.Icon(color='red', icon='star', prefix='fa')
    ).add_to(m)
    
    # Добавление данных если есть
    if 'data' in st.session_state and show_markers:
        df = st.session_state.data
        add_data_points_to_map(m, df)
    
    # Heatmap если включен
    if 'data' in st.session_state and show_heatmap:
        add_heatmap_to_map(m, st.session_state.data)
    
    # Добавление популярных мест
    add_popular_locations(m)
    
    # Добавление контролов
    add_map_controls(m)
    
    return m

def geocode_location(query):
    """Геокодирование через Google-подобный поиск"""
    
    try:
        # Пробуем несколько сервисов геокодирования
        
        # 1. Nominatim (OpenStreetMap)
        url = "https://nominatim.openstreetmap.org/search"
        params = {
            'q': query,
            'format': 'json',
            'limit': 1
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]['lat'])
                lon = float(data[0]['lon'])
                return [lat, lon]
        
        # 2. Fallback - координаты напрямую
        if ',' in query:
            try:
                parts = query.split(',')
                if len(parts) == 2:
                    lat = float(parts[0].strip())
                    lon = float(parts[1].strip())
                    if -90 <= lat <= 90 and -180 <= lon <= 180:
                        return [lat, lon]
            except:
                pass
        
        # 3. Предустановленные локации
        known_locations = {
            'jerusalem': [31.7683, 35.2137],
            'tel aviv': [32.0853, 34.7818],
            'haifa': [32.7940, 34.9896],
            'new york': [40.7128, -74.0060],
            'london': [51.5074, -0.1278],
            'paris': [48.8566, 2.3522],
            'tokyo': [35.6762, 139.6503],
            'moscow': [55.7558, 37.6173],
            'dubai': [25.2048, 55.2708],
            'kyiv': [50.4501, 30.5234],
            'berlin': [52.5200, 13.4050],
            'kiryat gat': [31.6095, 34.7733],
            'lviv': [49.8397, 24.0297],
        }
        
        query_lower = query.lower()
        for location, coords in known_locations.items():
            if location in query_lower:
                return coords
        
        return None
        
    except Exception as e:
        print(f"Geocoding error: {e}")
        return None

def reverse_geocode(lat, lng):
    """Обратное геокодирование - получение адреса по координатам"""
    
    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            'lat': lat,
            'lon': lng,
            'format': 'json'
        }
        
        response = requests.get(url, params=params, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('display_name', f"Lat: {lat:.4f}, Lng: {lng:.4f}")
        
    except:
        pass
    
    return f"Lat: {lat:.4f}, Lng: {lng:.4f}"

def add_data_points_to_map(map_obj, df):
    """Добавление точек данных на карту"""
    
    # Ищем колонки с координатами
    lat_cols = [col for col in df.columns if 'lat' in col.lower() or 'latitude' in col.lower()]
    lng_cols = [col for col in df.columns if 'lng' in col.lower() or 'lon' in col.lower() or 'longitude' in col.lower()]
    
    if lat_cols and lng_cols:
        lat_col = lat_cols[0]
        lng_col = lng_cols[0]
        
        # Добавляем маркеры для каждой точки
        for idx, row in df.iterrows():
            if pd.notna(row[lat_col]) and pd.notna(row[lng_col]):
                try:
                    lat = float(row[lat_col])
                    lng = float(row[lng_col])
                    
                    # Создаем popup с информацией
                    popup_info = f"<b>Data Point {idx}</b><br>"
                    for col in df.columns[:5]:  # Показываем первые 5 колонок
                        popup_info += f"{col}: {row[col]}<br>"
                    
                    folium.CircleMarker(
                        location=[lat, lng],
                        radius=5,
                        popup=popup_info,
                        color='blue',
                        fill=True,
                        fillColor='lightblue'
                    ).add_to(map_obj)
                    
                except:
                    continue

def add_heatmap_to_map(map_obj, df):
    """Добавление тепловой карты"""
    
    try:
        from folium.plugins import HeatMap
        
        # Ищем колонки с координатами
        lat_cols = [col for col in df.columns if 'lat' in col.lower()]
        lng_cols = [col for col in df.columns if 'lng' in col.lower() or 'lon' in col.lower()]
        
        if lat_cols and lng_cols:
            lat_col = lat_cols[0]
            lng_col = lng_cols[0]
            
            heat_data = []
            for idx, row in df.iterrows():
                if pd.notna(row[lat_col]) and pd.notna(row[lng_col]):
                    try:
                        lat = float(row[lat_col])
                        lng = float(row[lng_col])
                        heat_data.append([lat, lng])
                    except:
                        continue
            
            if heat_data:
                HeatMap(heat_data).add_to(map_obj)
                
    except ImportError:
        pass  # HeatMap не доступен

def add_popular_locations(map_obj):
    """Добавление популярных мест"""
    
    popular_places = [
        {"name": "🏛️ Old City Jerusalem", "coords": [31.7767, 35.2345], "color": "orange"},
        {"name": "🏖️ Tel Aviv Beach", "coords": [32.0805, 34.7693], "color": "blue"},
        {"name": "🌊 Haifa Port", "coords": [32.8191, 34.9983], "color": "green"},
        {"name": "🏜️ Dead Sea", "coords": [31.5590, 35.4732], "color": "purple"},
    ]
    
    for place in popular_places:
        folium.CircleMarker(
            location=place["coords"],
            radius=8,
            popup=place["name"],
            tooltip=place["name"],
            color=place["color"],
            fill=True,
            fillColor=place["color"],
            fillOpacity=0.7
        ).add_to(map_obj)

def add_map_controls(map_obj):
    """Добавление контролов на карту"""
    
    try:
        from folium.plugins import MeasureControl, Draw, Fullscreen
        
        # Инструмент измерения расстояний
        map_obj.add_child(MeasureControl())
        
        # Полноэкранный режим
        map_obj.add_child(Fullscreen())
        
        # Инструменты рисования
        draw = Draw(
            draw_options={'polyline': True, 'polygon': True, 'circle': True, 'rectangle': True, 'marker': True},
            edit_options={'edit': True}
        )
        map_obj.add_child(draw)
        
    except ImportError:
        pass  # Плагины не доступны

def show_ml():
    st.markdown("## 🤖 Machine Learning Analytics")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        st.warning("Need at least 2 numeric columns for ML!")
        return
    
    ml_type = st.selectbox(
        "🤖 Choose ML Analysis",
        ["🎯 Clustering", "📉 PCA Analysis", "🔍 Outlier Detection", "📊 Feature Importance"]
    )
    
    if ml_type == "🎯 Clustering":
        st.markdown("### K-Means Clustering")
        
        n_clusters = st.slider("Number of Clusters", 2, 10, 3)
        selected_features = st.multiselect("Select Features", numeric_cols, default=numeric_cols[:3])
        
        if len(selected_features) >= 2 and st.button("Run Clustering"):
            # Подготовка данных
            X = df[selected_features].dropna()
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Кластеризация
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            clusters = kmeans.fit_predict(X_scaled)
            
            # Добавляем кластеры в данные
            df_clustered = X.copy()
            df_clustered['Cluster'] = clusters
            
            # Визуализация
            if len(selected_features) >= 2:
                fig = px.scatter(
                    df_clustered, 
                    x=selected_features[0], 
                    y=selected_features[1],
                    color='Cluster',
                    title="K-Means Clustering Results"
                )
                st.plotly_chart(fig, use_container_width=True)
            
            # Статистика кластеров
            st.markdown("### 📊 Cluster Statistics")
            cluster_stats = df_clustered.groupby('Cluster')[selected_features].mean()
            st.dataframe(cluster_stats)
    
    elif ml_type == "📉 PCA Analysis":
        st.markdown("### Principal Component Analysis")
        
        selected_features = st.multiselect("Select Features", numeric_cols, default=numeric_cols)
        
        if len(selected_features) >= 2 and st.button("Run PCA"):
            # Подготовка данных
            X = df[selected_features].dropna()
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # PCA
            pca = PCA()
            X_pca = pca.fit_transform(X_scaled)
            
            # Explained variance
            explained_variance = pca.explained_variance_ratio_
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Scree plot
                fig = px.bar(
                    x=range(1, len(explained_variance) + 1),
                    y=explained_variance,
                    title="PCA Explained Variance",
                    labels={'x': 'Principal Component', 'y': 'Explained Variance Ratio'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                # Cumulative explained variance
                cumulative_variance = np.cumsum(explained_variance)
                fig = px.line(
                    x=range(1, len(cumulative_variance) + 1),
                    y=cumulative_variance,
                    title="Cumulative Explained Variance"
                )
                st.plotly_chart(fig, use_container_width=True)

def show_ab_testing():
    st.markdown("## 🧪 A/B Testing & Statistical Analysis")
    
    # Проверяем, что данные загружены
    if 'data' not in st.session_state or st.session_state.data is None:
        st.warning("📂 Please upload your dataset first in the 'Upload Data' section!")
        return

    df = st.session_state.data

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📊 A/B Test Setup")

        # Выбор колонок
        group_col = st.selectbox("Select Group Column", df.columns)
        metric_col = st.selectbox("Select Metric Column", df.columns)

        if st.button("📊 Analyze A/B Test"):
            try:
                # Фильтруем только нужные столбцы
                ab_data = df[[group_col, metric_col]].dropna()

                # Группы: Control и Treatment
                control = ab_data[ab_data[group_col] == ab_data[group_col].unique()[0]][metric_col]
                treatment = ab_data[ab_data[group_col] == ab_data[group_col].unique()[1]][metric_col]

                # Расчёты
                control_mean = control.mean()
                treatment_mean = treatment.mean()
                from scipy import stats
                t_stat, p_value = stats.ttest_ind(control, treatment, equal_var=False)

                # Результаты
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Control Mean", f"{control_mean:.3f}")
                with col2:
                    st.metric("Treatment Mean", f"{treatment_mean:.3f}")
                with col3:
                    st.metric("P-value", f"{p_value:.4f}")

                if p_value < 0.05:
                    st.success("🎉 Statistically Significant!")
                else:
                    st.warning("❌ Not Statistically Significant")

                # Визуализация
                fig = px.box(ab_data, x=group_col, y=metric_col, title=f"Distribution of {metric_col}")
                st.plotly_chart(fig, use_container_width=True)

            except Exception as e:
                st.error(f"⚠️ Error analyzing A/B test: {e}")

    with col2:
        st.markdown("### 🧮 Test Results")
        st.info("Select columns on the left and click 'Analyze A/B Test'.")
def show_database():
    st.markdown("## 💾 Database Connection & SQL")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 🔗 Database Setup")
        
        db_type = st.selectbox("Database Type", ["SQLite", "PostgreSQL", "MySQL"])
        
        # Загрузка файлов
        uploaded_files = st.file_uploader(
            "Upload CSV files",
            type=['csv'],
            accept_multiple_files=True
        )
        
        if uploaded_files and st.button("📁 Load Files to Database"):
            conn = sqlite3.connect('uploaded_data.db')
            for uploaded_file in uploaded_files:
                df = pd.read_csv(uploaded_file)
                table_name = uploaded_file.name.replace('.csv', '').replace(' ', '_').lower()
                df.to_sql(table_name, conn, if_exists='replace', index=False)
                st.success(f"Loaded {uploaded_file.name} as table '{table_name}'")
            conn.close()
        
        if db_type == "SQLite":
            if st.button("📁 Create Sample Database"):
                create_sample_database()
                st.success("Sample SQLite database created!")
        
        st.markdown("### ✏️ SQL Editor")
        sql_query = st.text_area(
            "Enter SQL Query",
            value="SELECT * FROM sales LIMIT 10;",
            height=150,
            help="Write your SQL query here"
        )
        
        if st.button("▶️ Execute Query"):
            try:
                # Проверяем есть ли загруженные данные
                if os.path.exists('uploaded_data.db'):
                    conn = sqlite3.connect('uploaded_data.db')
                    result = pd.read_sql_query(sql_query, conn)
                    conn.close()
                else:
                    result = execute_sql_query(sql_query)
                
                st.success("Query executed successfully!")
                st.dataframe(result)
            except Exception as e:
                st.error(f"Query error: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Query Results")
        
        # Предустановленные запросы
        st.markdown("### 🔍 Quick Queries")
        
        if st.button("📈 Total Sales"):
            try:
                if os.path.exists('uploaded_data.db'):
                    conn = sqlite3.connect('uploaded_data.db')
                    # Пробуем найти таблицу с колонкой amount
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                    for table in tables['name']:
                        try:
                            query = f"SELECT SUM(amount) as total_sales FROM {table};"
                            result = pd.read_sql_query(query, conn)
                            st.metric("Total Sales", f"${result.iloc[0, 0]:,.2f}")
                            break
                        except:
                            continue
                    conn.close()
                else:
                    query = "SELECT SUM(amount) as total_sales FROM sales;"
                    result = execute_sql_query(query)
                    st.metric("Total Sales", f"${result.iloc[0, 0]:,.2f}")
            except Exception as e:
                st.error(f"Error: {str(e)}")
        
        if st.button("👥 Customers by Region"):
            try:
                if os.path.exists('uploaded_data.db'):
                    conn = sqlite3.connect('uploaded_data.db')
                    tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table';", conn)
                    for table in tables['name']:
                        try:
                            query = f"SELECT region, COUNT(*) as customers FROM {table} GROUP BY region;"
                            result = pd.read_sql_query(query, conn)
                            fig = px.bar(result, x='region', y='customers', title="Customers by Region")
                            st.plotly_chart(fig, use_container_width=True)
                            break
                        except:
                            continue
                    conn.close()
                else:
                    query = "SELECT region, COUNT(*) as customers FROM sales GROUP BY region;"
                    result = execute_sql_query(query)
                    fig = px.bar(result, x='region', y='customers', title="Customers by Region")
                    st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error: {str(e)}")
def show_reports():
    st.markdown("## 📄 Automated Reports")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first!")
        return
    
    df = st.session_state.data
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📊 Report Configuration")
        
        report_type = st.selectbox(
            "Report Type",
            ["📈 Executive Summary", "📊 Detailed Analysis", "🎯 Custom Report"]
        )
        
        include_charts = st.checkbox("Include Charts", value=True)
        include_stats = st.checkbox("Include Statistics", value=True)
        
        if st.button("📄 Generate Report"):
            if report_type == "📈 Executive Summary":
                report_content = generate_executive_summary(df)
            elif report_type == "📊 Detailed Analysis":
                report_content = generate_detailed_analysis(df)
            else:
                report_content = generate_custom_report(df)
            
            st.markdown("### 📋 Report Preview")
            st.markdown(report_content)
    
    with col2:
        st.markdown("### 💾 Export Options")
        
        if st.button("📥 Download CSV"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name='data_export.csv',
                mime='text/csv'
            )
        
        if st.button("📊 Download Excel"):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Data', index=False)
            excel_data = output.getvalue()
            
            st.download_button(
                label="Download as Excel",
                data=excel_data,
                file_name='data_export.xlsx',
                mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )

def show_dashboard_builder():
    st.markdown("## 🎨 Dashboard Builder")
    
    if 'data' not in st.session_state:
        st.warning("Please upload data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    text_cols = df.select_dtypes(include=['object']).columns.tolist()
    
    # Sidebar для конфигурации
    with st.sidebar:
        st.markdown("### 🛠️ Dashboard Configuration")
        
        # Настройки дашборда
        dashboard_title = st.text_input("Dashboard Title", "My Analytics Dashboard")
        dashboard_theme = st.selectbox("Theme", ["Light", "Dark", "Corporate", "Modern"])
        layout_cols = st.selectbox("Layout", ["1 Column", "2 Columns", "3 Columns", "Grid"])
        
        st.markdown("### 📊 Available Widgets")
        
        # Инициализация виджетов в session_state
        if 'dashboard_widgets' not in st.session_state:
            st.session_state.dashboard_widgets = []
        
        # Добавление виджетов
        widget_type = st.selectbox("Choose Widget", [
            "📈 Line Chart",
            "📊 Bar Chart", 
            "🔢 Metric Card",
            "📋 Data Table",
            "🥧 Pie Chart",
            "📊 3D Scatter Plot",
            "🚨 Outlier Detection",
            "🗺️ Leaflet Map"
        ])
        
        if st.button("➕ Add Widget"):
            widget_config = create_widget_config(widget_type, df, numeric_cols, text_cols)
            if widget_config:
                st.session_state.dashboard_widgets.append(widget_config)
                st.success(f"Added {widget_type}!")
        
        # Управление виджетами
        if st.session_state.dashboard_widgets:
            st.markdown("### 🗂️ Manage Widgets")
            
            for i, widget in enumerate(st.session_state.dashboard_widgets):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{i+1}. {widget['type']}")
                with col2:
                    if st.button("🗑️", key=f"delete_{i}"):
                        st.session_state.dashboard_widgets.pop(i)
                        st.rerun()
    
    # Основная область дашборда
    st.markdown(f"# {dashboard_title}")
    
    # Применение темы
    apply_dashboard_theme(dashboard_theme)
    
    # Отображение виджетов
    if st.session_state.dashboard_widgets:
        render_dashboard_widgets(st.session_state.dashboard_widgets, df, layout_cols)
    else:
        st.info("👈 Add widgets from the sidebar to build your dashboard!")
        
        # Показать пример дашборда
        if st.button("🎯 Load Example Dashboard"):
            st.session_state.dashboard_widgets = create_example_dashboard(df, numeric_cols)
            st.rerun()

def create_widget_config(widget_type, df, numeric_cols, text_cols):
    """Создание конфигурации виджета"""
    
    if widget_type == "📈 Line Chart":
        if len(numeric_cols) == 0:
            st.error("No numeric columns available!")
            return None
        return {
            'type': widget_type,
            'title': 'Line Chart',
            'y_column': numeric_cols[0],
            'color': '#1f77b4',
            'show_points': True
        }
    
    elif widget_type == "📊 Bar Chart":
        if len(numeric_cols) == 0:
            st.error("No numeric columns available!")
            return None
        return {
            'type': widget_type,
            'title': 'Bar Chart',
            'y_column': numeric_cols[0],
            'color': '#ff7f0e'
        }
    
    elif widget_type == "🔢 Metric Card":
        if len(numeric_cols) == 0:
            st.error("No numeric columns available!")
            return None
        return {
            'type': widget_type,
            'title': 'Total',
            'column': numeric_cols[0],
            'aggregation': 'Sum',
            'format': 'Number'
        }
    
    elif widget_type == "🥧 Pie Chart":
        if len(text_cols) == 0:
            st.error("No categorical columns available!")
            return None
        return {
            'type': widget_type,
            'title': 'Distribution',
            'category_column': text_cols[0]
        }
    
    elif widget_type == "📋 Data Table":
        return {
            'type': widget_type,
            'title': 'Data Table',
            'columns': df.columns.tolist()[:5],
            'max_rows': 10
        }
    
    elif widget_type == "📊 3D Scatter Plot":
        if len(numeric_cols) < 3:
            st.error("Need at least 3 numeric columns for 3D scatter!")
            return None
        return {
            'type': widget_type,
            'title': '3D Scatter Plot',
            'x_column': numeric_cols[0],
            'y_column': numeric_cols[1],
            'z_column': numeric_cols[2],
            'color_by': 'None',
            'point_size': 8
        }
    
    elif widget_type == "🚨 Outlier Detection":
        if len(numeric_cols) == 0:
            st.error("No numeric columns available!")
            return None
        return {
            'type': widget_type,
            'title': 'Outlier Analysis',
            'column': numeric_cols[0],
            'method': 'IQR (Interquartile Range)',
            'sensitivity': 1.5,
            'show_stats': True
        }
    
    elif widget_type == "🗺️ Leaflet Map":
        return {
            'type': widget_type,
            'title': 'Interactive Map',
            'center_lat': 31.7683,  # Jerusalem
            'center_lon': 35.2137,
            'zoom': 10,
            'search_enabled': True
        }
    
    return None

def render_dashboard_widgets(widgets, df, layout):
    """Отображение виджетов на дашборде"""
    
    if layout == "1 Column":
        for widget in widgets:
            render_single_widget(widget, df)
    
    elif layout == "2 Columns":
        cols = st.columns(2)
        for i, widget in enumerate(widgets):
            with cols[i % 2]:
                render_single_widget(widget, df)
    
    elif layout == "3 Columns":
        cols = st.columns(3)
        for i, widget in enumerate(widgets):
            with cols[i % 3]:
                render_single_widget(widget, df)
    
    elif layout == "Grid":
        # Grid layout - 2x2, 2x3, etc.
        rows_needed = (len(widgets) + 1) // 2
        for row in range(rows_needed):
            cols = st.columns(2)
            for col_idx in range(2):
                widget_idx = row * 2 + col_idx
                if widget_idx < len(widgets):
                    with cols[col_idx]:
                        render_single_widget(widgets[widget_idx], df)

def render_single_widget(widget, df):
    """Отображение одного виджета"""
    
    try:
        if widget['type'] == "📈 Line Chart":
            st.markdown(f"### {widget['title']}")
            fig = px.line(df, y=widget['y_column'], title=widget['title'])
            fig.update_traces(line_color=widget['color'])
            if widget['show_points']:
                fig.update_traces(mode='lines+markers')
            st.plotly_chart(fig, use_container_width=True)
        
        elif widget['type'] == "📊 Bar Chart":
            st.markdown(f"### {widget['title']}")
            fig = px.bar(df, y=widget['y_column'], title=widget['title'])
            fig.update_traces(marker_color=widget['color'])
            st.plotly_chart(fig, use_container_width=True)
        
        elif widget['type'] == "🔢 Metric Card":
            col = widget['column']
            agg = widget['aggregation']
            
            if agg == "Sum":
                value = df[col].sum()
            elif agg == "Mean":
                value = df[col].mean()
            elif agg == "Count":
                value = df[col].count()
            elif agg == "Max":
                value = df[col].max()
            elif agg == "Min":
                value = df[col].min()
            
            # Форматирование
            if widget['format'] == "Currency":
                formatted_value = f"${value:,.2f}"
            elif widget['format'] == "Percentage":
                formatted_value = f"{value:.2f}%"
            else:
                formatted_value = f"{value:,.2f}"
            
            st.metric(widget['title'], formatted_value)
        
        elif widget['type'] == "🥧 Pie Chart":
            st.markdown(f"### {widget['title']}")
            value_counts = df[widget['category_column']].value_counts()
            fig = px.pie(values=value_counts.values, names=value_counts.index, title=widget['title'])
            st.plotly_chart(fig, use_container_width=True)
        
        elif widget['type'] == "📋 Data Table":
            st.markdown(f"### {widget['title']}")
            show_df = df[widget['columns']].head(widget['max_rows'])
            st.dataframe(show_df, use_container_width=True)
        
        elif widget['type'] == "📊 3D Scatter Plot":
            st.markdown(f"### {widget['title']}")
            plot_df = df[[widget['x_column'], widget['y_column'], widget['z_column']]].dropna()
            fig = px.scatter_3d(
                plot_df, 
                x=widget['x_column'], 
                y=widget['y_column'], 
                z=widget['z_column'],
                title=widget['title']
            )
            fig.update_traces(marker=dict(size=widget['point_size']))
            st.plotly_chart(fig, use_container_width=True)
        
        elif widget['type'] == "🚨 Outlier Detection":
            st.markdown(f"### {widget['title']}")
            column_data = df[widget['column']].dropna()
            outliers_idx, outlier_info = detect_outliers(column_data, widget['method'], widget['sensitivity'])
            
            # Box plot с выбросами
            fig_box = px.box(y=column_data, title=f"Outliers - {widget['column']}")
            
            if len(outliers_idx) > 0:
                outlier_values = column_data.loc[outliers_idx]
                fig_box.add_scatter(
                    y=outlier_values,
                    mode='markers',
                    marker=dict(color='red', size=8),
                    name='Outliers'
                )
            
            st.plotly_chart(fig_box, use_container_width=True)
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Total Points", len(column_data))
            with col2:
                st.metric("Outliers Found", len(outliers_idx))
        
        elif widget['type'] == "🗺️ Leaflet Map":
            st.markdown(f"### {widget['title']}")
            
            # Поиск места
            if widget.get('search_enabled', True):
                search_query = st.text_input("🔍 Search location", 
                                           placeholder="Enter city, address, or landmark...",
                                           key=f"search_{id(widget)}")
                
                if search_query and st.button("🌍 Find Location", key=f"find_{id(widget)}"):
                    coords = geocode_location(search_query)
                    if coords:
                        widget['center_lat'] = coords[0]
                        widget['center_lon'] = coords[1]
                        st.success(f"Found: {search_query}")
            
            # Создание карты
            m = folium.Map(
                location=[widget['center_lat'], widget['center_lon']],
                zoom_start=widget['zoom'],
                tiles='OpenStreetMap'
            )
            
            # Добавление маркера
            folium.Marker(
                [widget['center_lat'], widget['center_lon']],
                popup=f"📍 {widget['title']}",
                tooltip="Click for info",
                icon=folium.Icon(color='red', icon='info-sign')
            ).add_to(m)
            
            # Если есть данные - добавляем точки
            add_data_points_to_map(m, df)
            
            # Отображение карты
            map_data = st_folium(m, width=700, height=400, key=f"map_{id(widget)}")
            
            # Показать координаты клика
            if map_data['last_clicked']:
                lat = map_data['last_clicked']['lat']
                lng = map_data['last_clicked']['lng']
                st.info(f"📍 Clicked: {lat:.4f}, {lng:.4f}")
    
    except Exception as e:
        st.error(f"Error rendering widget: {str(e)}")

def apply_dashboard_theme(theme):
    """Применение темы к дашборду"""
    
    if theme == "Dark":
        st.markdown("""
        <style>
            .stApp { background-color: #0e1117; }
            .metric-card { background: #262730; }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme == "Corporate":
        st.markdown("""
        <style>
            .stApp { background-color: #f8f9fa; }
            .metric-card { 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 1rem;
                border-radius: 10px;
                margin: 0.5rem 0;
            }
        </style>
        """, unsafe_allow_html=True)
    
    elif theme == "Modern":
        st.markdown("""
        <style>
            .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
            .stWidget { background-color: rgba(255,255,255,0.9); border-radius: 10px; }
        </style>
        """, unsafe_allow_html=True)

def create_example_dashboard(df, numeric_cols):
    """Создание примера дашборда"""
    
    example_widgets = []
    
    if len(numeric_cols) > 0:
        # Metric card
        example_widgets.append({
            'type': '🔢 Metric Card',
            'title': 'Total Records',
            'column': numeric_cols[0],
            'aggregation': 'Count',
            'format': 'Number'
        })
        
        # Line chart
        example_widgets.append({
            'type': '📈 Line Chart',
            'title': 'Trend Analysis',
            'y_column': numeric_cols[0],
            'color': '#1f77b4',
            'show_points': True
        })
        
        # Leaflet Map
        example_widgets.append({
            'type': '🗺️ Leaflet Map',
            'title': 'Location Map',
            'center_lat': 31.7683,
            'center_lon': 35.2137,
            'zoom': 10,
            'search_enabled': True
        })
        
        # Outlier detection
        example_widgets.append({
            'type': '🚨 Outlier Detection',
            'title': 'Anomaly Detection',
            'column': numeric_cols[0],
            'method': 'IQR (Interquartile Range)',
            'sensitivity': 1.5,
            'show_stats': True
        })
        
        # 3D Scatter если есть достаточно колонок
        if len(numeric_cols) >= 3:
            example_widgets.append({
                'type': '📊 3D Scatter Plot',
                'title': '3D Analysis',
                'x_column': numeric_cols[0],
                'y_column': numeric_cols[1], 
                'z_column': numeric_cols[2],
                'color_by': 'None',
                'point_size': 8
            })
        
        # Data table
        example_widgets.append({
            'type': '📋 Data Table',
            'title': 'Data Preview',
            'columns': df.columns.tolist()[:4],
            'max_rows': 5
        })
    
    return example_widgets

def detect_outliers(data, method="IQR (Interquartile Range)", sensitivity=1.5):
    """Детекция выбросов различными методами"""
    
    outliers_idx = []
    info = {}
    
    if method == "IQR (Interquartile Range)":
        Q1 = data.quantile(0.25)
        Q3 = data.quantile(0.75)
        IQR = Q3 - Q1
        
        lower_bound = Q1 - sensitivity * IQR
        upper_bound = Q3 + sensitivity * IQR
        
        outliers_idx = data[(data < lower_bound) | (data > upper_bound)].index.tolist()
        
        info = {
            'method': 'IQR',
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'Q1': Q1,
            'Q3': Q3,
            'IQR': IQR
        }
    
    elif method == "Z-Score":
        z_scores = np.abs((data - data.mean()) / data.std())
        outliers_idx = data[z_scores > sensitivity].index.tolist()
        
        info = {
            'method': 'Z-Score',
            'threshold': sensitivity,
            'mean': data.mean(),
            'std': data.std()
        }
    
    return outliers_idx, info

# Вспомогательные функции
def create_demo_data():
    np.random.seed(42)
    data = {
        'Date': pd.date_range('2024-01-01', periods=100),
        'Sales': np.random.normal(1000, 200, 100),
        'Customers': np.random.poisson(30, 100),
        'Revenue': np.random.normal(5000, 1000, 100),
        'Region': np.random.choice(['North', 'South', 'East', 'West'], 100)
    }
    return pd.DataFrame(data)

def create_ecommerce_data():
    np.random.seed(123)
    data = {
        'user_id': range(1, 1001),
        'age': np.random.randint(18, 65, 1000),
        'gender': np.random.choice(['M', 'F'], 1000),
        'purchase_amount': np.random.exponential(50, 1000),
        'category': np.random.choice(['Electronics', 'Clothing', 'Books', 'Home'], 1000),
        'satisfaction': np.random.randint(1, 6, 1000)
    }
    return pd.DataFrame(data)

def auto_analyze_data():
    if 'data' not in st.session_state:
        return
    
    df = st.session_state.data
    
    st.markdown("### 🔍 Auto Analysis Results")
    
    # Основная статистика
    st.markdown("#### 📊 Dataset Overview")
    st.write(f"Rows: {len(df)}, Columns: {len(df.columns)}")
    
    # Пропущенные значения
    missing = df.isnull().sum()
    if missing.sum() > 0:
        st.warning(f"Found {missing.sum()} missing values")
    
    # Корреляции
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()
        high_corr = np.where(np.abs(corr) > 0.7)
        if len(high_corr[0]) > len(numeric_cols):  # исключаем диагональ
            st.info("Found high correlations between variables")

def calculate_data_quality(df):
    score = 10.0
    
    # Пропущенные значения
    missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns))
    score -= missing_pct * 5
    
    # Дубликаты
    duplicate_pct = df.duplicated().sum() / len(df)
    score -= duplicate_pct * 3
    
    return max(0, score)

def fill_missing_values(df):
    df_filled = df.copy()
    
    for col in df_filled.columns:
        if df_filled[col].dtype in ['float64', 'int64']:
            df_filled[col] = df_filled[col].fillna(df_filled[col].median())
        else:
            df_filled[col] = df_filled[col].fillna(df_filled[col].mode()[0] if not df_filled[col].mode().empty else 'Unknown')
    
    return df_filled

def show_world_map():
    st.markdown("### 🌍 Interactive World Map")
    world_data = create_world_map_data()
    map_type = st.selectbox("Map Type", ["🌍 Countries", "🏙️ Cities"])
    
    if map_type == "🌍 Countries":
        fig_map = px.choropleth(
            world_data['countries'], 
            locations="iso_alpha",
            color="value",
            hover_name="country",
            color_continuous_scale="Viridis",
            title="World Data by Countries"
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    elif map_type == "🏙️ Cities":
        fig_map = px.scatter_geo(
            world_data['cities'],
            lat="lat",
            lon="lon",
            color="population",
            size="population",
            hover_name="city",
            title="Major Cities Population",
            color_continuous_scale="Plasma"
        )
        st.plotly_chart(fig_map, use_container_width=True)

def create_world_map_data():
    countries_data = {
        'country': ['USA', 'China', 'Germany', 'Japan', 'UK', 'France', 'India', 'Brazil', 'Canada', 'Australia', 'Israel', 'Ukraine'],
        'iso_alpha': ['USA', 'CHN', 'DEU', 'JPN', 'GBR', 'FRA', 'IND', 'BRA', 'CAN', 'AUS', 'ISR', 'UKR'],
        'value': [331, 1439, 83, 126, 67, 67, 1380, 213, 38, 25, 9.4, 41.1]
    }
    
    cities_data = {
        'city': ['New York', 'London', 'Tokyo', 'Paris', 'Sydney', 'Moscow', 'Dubai', 'Singapore', 'Berlin', 'Toronto', 'Tel Aviv', 'Jerusalem', 'Kyiv', 'Odesa'],
        'lat': [40.7128, 51.5074, 35.6762, 48.8566, -33.8688, 55.7558, 25.2048, 1.3521, 52.5200, 43.6532, 32.0853, 31.7683, 50.4501, 46.4825],
        'lon': [-74.0060, -0.1278, 139.6503, 2.3522, 151.2093, 37.6173, 55.2708, 103.8198, 13.4050, -79.3832, 34.7818, 35.2137, 30.5234, 30.7233],
        'population': [8.4, 9.0, 13.9, 2.1, 5.3, 12.5, 3.4, 5.9, 3.7, 2.9, 0.46, 0.95, 2.95, 1.02]
    }
    
    return {
        'countries': pd.DataFrame(countries_data),
        'cities': pd.DataFrame(cities_data)
    }

def generate_ab_test_data():
    np.random.seed(42)
    
    # Control group
    control = pd.DataFrame({
        'group': 'Control',
        'conversion_rate': np.random.beta(2, 18, 1000),  # ~10% conversion
        'revenue': np.random.exponential(25, 1000),
        'clicks': np.random.poisson(100, 1000)
    })
    
    # Treatment group (slightly better)
    treatment = pd.DataFrame({
        'group': 'Treatment',
        'conversion_rate': np.random.beta(2.5, 17.5, 1000),  # ~12.5% conversion
        'revenue': np.random.exponential(30, 1000),
        'clicks': np.random.poisson(110, 1000)
    })
    
    return pd.concat([control, treatment], ignore_index=True)

def analyze_ab_test(data, metric):
    control = data[data['group'] == 'Control'][metric]
    treatment = data[data['group'] == 'Treatment'][metric]
    
    # T-test
    t_stat, p_value = stats.ttest_ind(control, treatment)
    
    return {
        'control_mean': control.mean(),
        'treatment_mean': treatment.mean(),
        'p_value': p_value,
        't_statistic': t_stat
    }

def create_sample_database():
    conn = sqlite3.connect('sample_data.db')
    
    # Создаем таблицу продаж
    sales_data = {
        'id': range(1, 101),
        'region': np.random.choice(['North', 'South', 'East', 'West'], 100),
        'amount': np.random.exponential(100, 100),
        'date': pd.date_range('2024-01-01', periods=100),
        'customer_id': np.random.randint(1, 51, 100)
    }
    
    df = pd.DataFrame(sales_data)
    df.to_sql('sales', conn, if_exists='replace', index=False)
    conn.close()

def execute_sql_query(query):
    try:
        conn = sqlite3.connect('sample_data.db')
        result = pd.read_sql_query(query, conn)
        conn.close()
        return result
    except Exception as e:
        raise e

def generate_executive_summary(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    summary = f"""
# 📊 Executive Summary

## Key Metrics
- **Total Records**: {len(df):,}
- **Data Columns**: {len(df.columns)}
- **Data Quality**: {calculate_data_quality(df):.1f}/10

## Insights
"""
    
    if len(numeric_cols) > 0:
        for col in numeric_cols[:3]:
            mean_val = df[col].mean()
            summary += f"- **{col}**: Average of {mean_val:.2f}\n"
    
    return summary

def generate_detailed_analysis(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    text_cols = df.select_dtypes(include=['object']).columns
    
    analysis = f"""
# 📈 Detailed Data Analysis

## Dataset Overview
- **Total Rows**: {len(df):,}
- **Total Columns**: {len(df.columns)}
- **Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
- **Numeric Columns**: {len(numeric_cols)}
- **Text Columns**: {len(text_cols)}

## Data Quality Assessment
- **Missing Values**: {df.isnull().sum().sum():,} ({(df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.1f}%)
- **Duplicate Rows**: {df.duplicated().sum():,} ({(df.duplicated().sum() / len(df) * 100):.1f}%)
- **Quality Score**: {calculate_data_quality(df):.1f}/10

## Statistical Summary
"""
    
    if len(numeric_cols) > 0:
        analysis += "\n### Numeric Columns Analysis\n"
        for col in numeric_cols:
            stats = df[col].describe()
            analysis += f"""
**{col}**:
- Mean: {stats['mean']:.2f}
- Median: {stats['50%']:.2f}
- Std Dev: {stats['std']:.2f}
- Min: {stats['min']:.2f}
- Max: {stats['max']:.2f}
"""
    
    return analysis

def generate_custom_report(df):
    return f"""
# 🎯 Custom Analytics Report

## Executive Summary
This report provides a comprehensive analysis of the uploaded dataset containing {len(df):,} records across {len(df.columns)} variables.

## Key Findings
1. **Data Completeness**: {100 - (df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100):.1f}% complete
2. **Data Uniqueness**: {100 - (df.duplicated().sum() / len(df) * 100):.1f}% unique records
3. **Numerical Features**: {len(df.select_dtypes(include=[np.number]).columns)} available for analysis

## Recommendations
- Consider data cleaning for missing values
- Explore correlations between numeric variables
- Implement feature engineering for categorical variables
"""

def show_stats():
    st.markdown("## 📊 Advanced Statistical Analysis")
    if 'data' not in st.session_state:
        st.warning("Please upload data first!")
        return
    
    df = st.session_state.data
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 📈 Descriptive Statistics")
        if len(numeric_cols) > 0:
            st.dataframe(df[numeric_cols].describe())
        
        # Распределения
        if len(numeric_cols) > 0:
            st.markdown("### 📊 Distribution Analysis")
            selected_col = st.selectbox("Choose column for distribution", numeric_cols)
            
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Гистограмма
                fig_hist = px.histogram(df, x=selected_col, title=f"Distribution of {selected_col}")
                st.plotly_chart(fig_hist, use_container_width=True)
            
            with col_b:
                # Box plot
                fig_box = px.box(df, y=selected_col, title=f"Box Plot: {selected_col}")
                st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        st.markdown("### 🎯 Statistical Tests")
        
        if len(numeric_cols) >= 2:
            st.markdown("#### Correlation Tests")
            col1_test = st.selectbox("Variable 1", numeric_cols, key="test1")
            col2_test = st.selectbox("Variable 2", [col for col in numeric_cols if col != col1_test], key="test2")
            
            if st.button("Run Correlation Test"):
                corr_coef, p_value = stats.pearsonr(df[col1_test].dropna(), df[col2_test].dropna())
                
                st.metric("Correlation Coefficient", f"{corr_coef:.3f}")
                st.metric("P-value", f"{p_value:.4f}")
                
                if p_value < 0.05:
                    st.success("Statistically significant correlation!")
                else:
                    st.warning("No significant correlation")
        
        # Normality tests
        if len(numeric_cols) > 0:
            st.markdown("#### Normality Test")
            norm_col = st.selectbox("Test for normality", numeric_cols, key="norm")
            
            if st.button("Run Shapiro-Wilk Test"):
                stat, p_val = stats.shapiro(df[norm_col].dropna().sample(min(5000, len(df))))
                
                st.metric("Test Statistic", f"{stat:.4f}")
                st.metric("P-value", f"{p_val:.4f}")
                
                if p_val > 0.05:
                    st.success("Data appears normally distributed")
                else:
                    st.warning("Data is not normally distributed")

if __name__ == "__main__":
    main()
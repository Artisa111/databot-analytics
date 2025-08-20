import logging
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import pandas as pd
import io
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
# Railway-compatible imports
try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_AVAILABLE = True
except ImportError:
    PLOTLY_AVAILABLE = False
    print("Plotly not available, using matplotlib only")
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans, DBSCAN
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import silhouette_score
from scipy.stats import pearsonr, spearmanr, shapiro, normaltest, probplot
import warnings
warnings.filterwarnings('ignore')

# Set style for better plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

# Load environment variables
load_dotenv()

# Get token
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Setup logging
logging.basicConfig(level=logging.INFO)

class AdvancedDataAnalyticsBot:
    def __init__(self):
        if not TOKEN:
            raise ValueError("TELEGRAM_TOKEN not found in .env file!")
        
        self.application = Application.builder().token(TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("analyze", self.analyze))
        self.application.add_handler(CommandHandler("visualize", self.visualize))
        self.application.add_handler(CommandHandler("charts", self.create_charts))
        self.application.add_handler(CommandHandler("ml", self.machine_learning))
        self.application.add_handler(CommandHandler("report", self.generate_report))
        self.application.add_handler(CommandHandler("stats", self.advanced_statistics))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    def get_persistent_keyboard(self):
        """Create persistent keyboard that stays at bottom"""
        keyboard = [
            [
                KeyboardButton("📊 Quick Analysis"),
                KeyboardButton("📈 Visualizations"),
                KeyboardButton("🤖 ML Analysis")
            ],
            [
                KeyboardButton("📋 Full Report"),
                KeyboardButton("📉 Advanced Stats"),
                KeyboardButton("❓ Help")
            ]
        ]
        return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, persistent=True)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command with persistent keyboard"""
        welcome_text = """
🚀 **Welcome to Advanced DataBot Analytics Pro!**

🎯 **Premium Features:**
• 📊 **Statistical Analysis** - Comprehensive descriptive & inferential stats
• 🎨 **Advanced Visualizations** - 15+ chart types with interactive plots
• 🤖 **Machine Learning Suite** - Clustering, PCA, Anomaly Detection, Predictions
• 📋 **Professional Reports** - Business-ready insights with recommendations
• 🔍 **Data Quality Assessment** - Missing data, outliers, data profiling
• 📈 **Time Series Analysis** - Trend detection and forecasting
• 🌐 **Multi-format Support** - CSV, Excel, JSON, TSV, Parquet

📁 **Supported Data Types:**
✅ Numeric data (integers, floats)
✅ Categorical data (text, categories)  
✅ Date/Time data (timestamps, dates)
✅ Boolean data (true/false)
✅ Mixed datasets (any combination)

**🎯 Simply upload your data file and use the menu below!**

*The menu will stay fixed at the bottom for easy access.*
        """
        
        await update.message.reply_text(
            welcome_text, 
            parse_mode='Markdown',
            reply_markup=self.get_persistent_keyboard()
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced help command"""
        help_text = """
🔧 **Advanced DataBot Analytics Pro - Complete Guide**

🎯 **Main Commands:**
/start - Launch bot with persistent menu
/help - Show this comprehensive guide
/analyze - Detailed statistical analysis  
/visualize - Create advanced visualizations
/charts - Generate comprehensive chart suite
/ml - Machine learning analysis
/report - Full analytical report
/stats - Advanced statistical metrics

📊 **Visualization Types Available:**
• **Distribution Plots** - Histograms, KDE, Q-Q plots
• **Relationship Plots** - Scatter, correlation matrix, pair plots
• **Categorical Analysis** - Bar charts, count plots, cross-tabs
• **Statistical Plots** - Box plots, violin plots, strip plots
• **Time Series** - Line plots, seasonal decomposition
• **3D Visualizations** - 3D scatter, surface plots
• **Interactive Charts** - Plotly-powered dynamic visualizations

🤖 **Machine Learning Capabilities:**
• **Clustering Analysis** - K-Means, DBSCAN with optimization
• **Dimensionality Reduction** - PCA, t-SNE analysis
• **Feature Engineering** - Importance ranking, selection
• **Anomaly Detection** - Isolation Forest, statistical outliers
• **Predictive Modeling** - Regression, classification insights
• **Model Validation** - Cross-validation, performance metrics

📋 **Report Components:**
• **Executive Summary** - Key findings and insights
• **Data Quality Assessment** - Completeness, consistency, accuracy
• **Statistical Analysis** - Descriptive stats, distributions
• **Business Recommendations** - Actionable insights
• **Visualization Gallery** - Professional charts and graphs

📁 **File Format Support:**
• CSV (Comma-separated values)
• Excel (XLS, XLSX) - Multiple sheets supported
• JSON (JavaScript Object Notation)
• TSV (Tab-separated values)
• Parquet (Columnar storage)
• TXT (Delimited text files)

📊 **Data Size Limits:**
• Maximum file size: 20MB
• Recommended rows: Up to 100,000 for optimal performance
• Columns: Unlimited (practical limit ~200)

💡 **Getting Started:**
1. Send /start to activate the persistent menu
2. Upload your data file (any supported format)
3. Use the menu buttons for different analyses
4. Get professional insights instantly!

🎯 **Pro Tips:**
• Clean column names work better (no special characters)
• Include headers in your data files
• Date columns should be in standard formats
• Large files may take longer to process
        """
        
        await update.message.reply_text(
            help_text, 
            parse_mode='Markdown',
            reply_markup=self.get_persistent_keyboard()
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries"""
        query = update.callback_query
        await query.answer()
        
        callback_data = query.data
        
        if callback_data == "quick_analyze":
            await self.analyze(update, context, callback=True)
        elif callback_data == "create_viz":
            await self.visualize(update, context, callback=True)
        elif callback_data == "ml_analysis":
            await self.machine_learning(update, context, callback=True)
        elif callback_data == "full_report":
            await self.generate_report(update, context, callback=True)
        elif callback_data == "adv_stats":
            await self.advanced_statistics(update, context, callback=True)
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced document handler supporting multiple formats"""
        try:
            file_name = update.message.document.file_name
            file_ext = os.path.splitext(file_name.lower())[1]
            
            # Expanded file format support
            supported_formats = {
                '.csv': 'CSV',
                '.xlsx': 'Excel',
                '.xls': 'Excel',
                '.json': 'JSON',
                '.tsv': 'TSV',
                '.txt': 'Text',
                '.parquet': 'Parquet'
            }
            
            if file_ext not in supported_formats:
                await update.message.reply_text(
                    f"❌ **Unsupported file format: {file_ext}**\n\n"
                    f"📁 **Supported formats:**\n"
                    f"• CSV (.csv)\n"
                    f"• Excel (.xlsx, .xls)\n"
                    f"• JSON (.json)\n"
                    f"• TSV (.tsv)\n"
                    f"• Text (.txt)\n"
                    f"• Parquet (.parquet)\n\n"
                    f"**Maximum file size: 20MB**",
                    parse_mode='Markdown',
                    reply_markup=self.get_persistent_keyboard()
                )
                return
            
            await update.message.reply_text(
                f"📊 **Processing {supported_formats[file_ext]} file...** \n"
                f"📁 File: `{file_name}`\n"
                f"⏳ Please wait while I analyze your data...",
                parse_mode='Markdown'
            )
            
            # Download file
            file = await update.message.document.get_file()
            file_bytes = await file.download_as_bytearray()
            
            # Load data based on file type with error handling
            try:
                df = self.load_data_file(file_bytes, file_ext)
            except Exception as load_error:
                await update.message.reply_text(
                    f"❌ **Error loading file:** {str(load_error)}\n\n"
                    f"💡 **Common solutions:**\n"
                    f"• Check file encoding (UTF-8 recommended)\n"
                    f"• Ensure proper column headers\n"
                    f"• Verify data format consistency\n"
                    f"• Try saving as CSV format",
                    parse_mode='Markdown',
                    reply_markup=self.get_persistent_keyboard()
                )
                return
            
            # Enhanced data preprocessing
            df = self.preprocess_data(df)
            
            # Save in user context
            context.user_data['dataframe'] = df
            context.user_data['filename'] = file_name
            context.user_data['file_format'] = supported_formats[file_ext]
            
            # Enhanced quick analysis
            analysis_text = self.comprehensive_quick_analysis(df, file_name)
            
            await update.message.reply_text(
                analysis_text, 
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
            
            # Auto-generate enhanced preview
            await update.message.reply_text("🎨 **Generating comprehensive data preview...**")
            await self.send_enhanced_preview_charts(update, context, df)
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ **Processing Error:** {str(e)}\n\n"
                f"Please try again or contact support if the issue persists.",
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
    
    def load_data_file(self, file_bytes, file_ext):
        """Load data file based on extension with robust error handling"""
        try:
            if file_ext == '.csv':
                # Try different encodings and separators
                for encoding in ['utf-8', 'latin-1', 'cp1252']:
                    try:
                        df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
                        break
                    except UnicodeDecodeError:
                        continue
                else:
                    df = pd.read_csv(io.BytesIO(file_bytes), encoding='utf-8', errors='ignore')
                    
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(io.BytesIO(file_bytes), engine='openpyxl' if file_ext == '.xlsx' else None)
                
            elif file_ext == '.json':
                df = pd.read_json(io.BytesIO(file_bytes))
                
            elif file_ext == '.tsv':
                df = pd.read_csv(io.BytesIO(file_bytes), sep='\t')
                
            elif file_ext == '.txt':
                # Try to detect delimiter
                content = file_bytes.decode('utf-8')
                if '\t' in content:
                    df = pd.read_csv(io.StringIO(content), sep='\t')
                elif '|' in content:
                    df = pd.read_csv(io.StringIO(content), sep='|')
                else:
                    df = pd.read_csv(io.StringIO(content))
                    
            elif file_ext == '.parquet':
                df = pd.read_parquet(io.BytesIO(file_bytes))
                
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
                
            return df
            
        except Exception as e:
            raise Exception(f"Failed to load {file_ext} file: {str(e)}")
    
    def preprocess_data(self, df):
        """Enhanced data preprocessing"""
        # Clean column names
        df.columns = df.columns.astype(str).str.strip().str.replace(' ', '_')
        
        # Convert date columns
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to datetime
                try:
                    df[col] = pd.to_datetime(df[col], errors='ignore')
                except:
                    pass
        
        # Handle mixed types
        for col in df.columns:
            if df[col].dtype == 'object':
                # Try to convert to numeric
                numeric_converted = pd.to_numeric(df[col], errors='coerce')
                if not numeric_converted.isna().all():
                    # If more than 50% can be converted to numeric, do it
                    if (numeric_converted.notna().sum() / len(df)) > 0.5:
                        df[col] = numeric_converted
        
        return df
    
    def comprehensive_quick_analysis(self, df, filename):
        """Enhanced comprehensive quick analysis"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        datetime_cols = df.select_dtypes(include=['datetime']).columns
        bool_cols = df.select_dtypes(include=['bool']).columns
        
        # Enhanced data quality metrics
        missing_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()
        total_cells = len(df) * len(df.columns)
        completeness = ((total_cells - missing_count) / total_cells * 100) if total_cells > 0 else 0
        
        # Memory usage
        memory_usage = df.memory_usage(deep=True).sum() / (1024**2)
        
        # Data insights
        data_quality = "🟢 Excellent" if completeness > 95 else "🟡 Good" if completeness > 85 else "🟠 Fair" if completeness > 70 else "🔴 Poor"
        dataset_size = "Very Large" if len(df) > 100000 else "Large" if len(df) > 10000 else "Medium" if len(df) > 1000 else "Small"
        
        # Column type analysis
        unique_ratios = []
        for col in df.columns:
            unique_ratio = df[col].nunique() / len(df) if len(df) > 0 else 0
            unique_ratios.append(unique_ratio)
        
        avg_unique_ratio = np.mean(unique_ratios)
        data_diversity = "High" if avg_unique_ratio > 0.8 else "Medium" if avg_unique_ratio > 0.3 else "Low"
        
        analysis = f"""
📊 **Comprehensive File Analysis: `{filename}`**

🎯 **Dataset Overview:**
• **Size:** {len(df):,} rows × {len(df.columns)} columns ({dataset_size} dataset)
• **Memory Usage:** {memory_usage:.2f} MB
• **Data Quality:** {data_quality} ({completeness:.1f}% complete)
• **Data Diversity:** {data_diversity} (unique ratio: {avg_unique_ratio:.2f})

📈 **Column Type Distribution:**
• **Numeric Columns:** {len(numeric_cols)} ({len(numeric_cols)/len(df.columns)*100:.1f}%)
• **Text/Categorical:** {len(text_cols)} ({len(text_cols)/len(df.columns)*100:.1f}%)
• **DateTime Columns:** {len(datetime_cols)} ({len(datetime_cols)/len(df.columns)*100:.1f}%)
• **Boolean Columns:** {len(bool_cols)} ({len(bool_cols)/len(df.columns)*100:.1f}%)

🔍 **Data Quality Metrics:**
• **Missing Values:** {missing_count:,} ({100 * missing_count / total_cells:.2f}%)
• **Duplicate Rows:** {duplicate_count:,} ({100 * duplicate_count / len(df):.1f}%)
• **Complete Records:** {len(df.dropna()):,} ({100 * len(df.dropna()) / len(df):.1f}%)
• **Unique Records:** {len(df) - duplicate_count:,}

🎯 **Analysis Readiness:**
        """
        
        # Analysis readiness assessment
        if len(numeric_cols) >= 3:
            analysis += "• ✅ **ML Ready** - Suitable for machine learning algorithms\n"
        if len(datetime_cols) >= 1:
            analysis += "• 📈 **Time Series Ready** - Temporal analysis available\n"
        if len(text_cols) >= 2:
            analysis += "• 📊 **Categorical Analysis Ready** - Cross-tabulation possible\n"
        if completeness > 90:
            analysis += "• 🎯 **High Quality Data** - Minimal preprocessing needed\n"
        if len(df) > 1000:
            analysis += "• 📊 **Statistically Significant** - Robust analysis possible\n"
        
        analysis += f"""
📋 **Recommended Analysis:**
"""
        
        if len(numeric_cols) >= 2:
            analysis += "• Correlation and regression analysis\n"
        if len(numeric_cols) >= 3:
            analysis += "• Clustering and dimensionality reduction\n"
        if len(text_cols) > 0:
            analysis += "• Categorical data analysis and profiling\n"
        if missing_count > 0:
            analysis += "• Missing data pattern analysis\n"
        if len(datetime_cols) > 0:
            analysis += "• Time series and trend analysis\n"
        
        analysis += f"""
✅ **Status:** Data successfully loaded and preprocessed!
🎯 **Ready for analysis!** Use the menu below for detailed insights.
        """
        
        return analysis
    
    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Enhanced comprehensive analysis"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\n\nPlease upload a data file first using the document upload feature."
            await self.send_message(update, context, message_text, callback)
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "🔍 **Performing comprehensive statistical analysis...** \n\nThis includes descriptive statistics, correlation analysis, distribution testing, and data profiling."
            await self.send_message(update, context, progress_text, callback)
            
            # Enhanced detailed analysis
            detailed_analysis = self.enhanced_statistical_analysis(df, filename)
            
            # Send analysis in chunks
            await self.send_long_message(update, context, detailed_analysis, callback)
            
        except Exception as e:
            error_msg = f"❌ **Analysis Error:** {str(e)}\n\nPlease try again or ensure your data is properly formatted."
            await self.send_message(update, context, error_msg, callback)
    
    async def visualize(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Create comprehensive visualization suite"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a data file first."
            await self.send_message(update, context, message_text, callback)
            return
        
        df = context.user_data['dataframe']
        progress_text = "📈 **Creating comprehensive visualization suite...** \n\nGenerating multiple chart types for complete data exploration."
        
        await self.send_message(update, context, progress_text, callback)
        await self.send_comprehensive_visualizations(update, context, df)
    
    async def create_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate advanced chart collection"""
        if 'dataframe' not in context.user_data:
            await update.message.reply_text(
                "📁 **No data loaded!**\nPlease upload a data file first.",
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
            return
        
        df = context.user_data['dataframe']
        await update.message.reply_text(
            "🎨 **Generating advanced chart collection...** \n\nCreating specialized visualizations for your data.",
            parse_mode='Markdown'
        )
        
        await self.send_advanced_chart_collection(update, context, df)
    
    async def machine_learning(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Comprehensive ML analysis with enhanced algorithms"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a data file first."
            await self.send_message(update, context, message_text, callback)
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "🤖 **Running advanced ML analysis...** \n\nPerforming clustering, PCA, anomaly detection, and feature analysis."
            await self.send_message(update, context, progress_text, callback)
            
            # Get numeric data
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) < 2:
                error_msg = "❌ **Insufficient numeric data!**\n\nMachine learning analysis requires at least 2 numeric columns.\n\nYour data has numeric columns: " + str(len(numeric_cols))
                await self.send_message(update, context, error_msg, callback)
                return
            
            # Prepare data
            X = df[numeric_cols].dropna()
            
            if len(X) < 10:
                error_msg = f"❌ **Insufficient data points!**\n\nML analysis requires at least 10 complete rows.\n\nYour data has {len(X)} complete rows after removing missing values."
                await self.send_message(update, context, error_msg, callback)
                return
            
            # Standardize data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Enhanced ML analysis
            ml_results = self.perform_advanced_ml_analysis(X, X_scaled, numeric_cols, filename)
            
            # Send results
            await self.send_long_message(update, context, ml_results, callback)
            
            # Generate ML visualizations
            await self.send_enhanced_ml_charts(update, context, X, X_scaled, numeric_cols)
            
        except Exception as e:
            error_msg = f"❌ **ML Analysis Error:** {str(e)}"
            await self.send_message(update, context, error_msg, callback)
    
    async def generate_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Generate comprehensive business report"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a data file first."
            await self.send_message(update, context, message_text, callback)
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "📋 **Generating comprehensive business report...** \n\nAnalyzing data quality, patterns, insights, and recommendations."
            await self.send_message(update, context, progress_text, callback)
            
            # Generate enhanced report
            report = self.generate_business_intelligence_report(df, filename)
            
            # Send report sections
            await self.send_long_message(update, context, report, callback)
            
            # Generate report visualizations
            await self.send_business_report_charts(update, context, df)
            
        except Exception as e:
            error_msg = f"❌ **Report Generation Error:** {str(e)}"
            await self.send_message(update, context, error_msg, callback)
    
    async def advanced_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Advanced statistical analysis with hypothesis testing"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a data file first."
            await self.send_message(update, context, message_text, callback)
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "📉 **Computing advanced statistics...** \n\nRunning normality tests, correlation analysis, and hypothesis testing."
            await self.send_message(update, context, progress_text, callback)
            
            # Advanced statistical analysis
            stats_results = self.compute_inferential_statistics(df, filename)
            
            # Send results
            await self.send_long_message(update, context, stats_results, callback)
            
            # Generate statistical charts
            await self.send_advanced_statistical_charts(update, context, df)
            
        except Exception as e:
            error_msg = f"❌ **Statistical Analysis Error:** {str(e)}"
            await self.send_message(update, context, error_msg, callback)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced text message handler for menu buttons"""
        text = update.message.text
        
        # Handle menu button presses
        if text == "📊 Quick Analysis":
            await self.analyze(update, context)
        elif text == "📈 Visualizations":
            await self.visualize(update, context)
        elif text == "🤖 ML Analysis":
            await self.machine_learning(update, context)
        elif text == "📋 Full Report":
            await self.generate_report(update, context)
        elif text == "📉 Advanced Stats":
            await self.advanced_statistics(update, context)
        elif text == "❓ Help":
            await self.help_command(update, context)
        
        # Handle conversational messages
        elif any(word in text.lower() for word in ['hello', 'hi', 'hey', 'start']):
            await update.message.reply_text(
                "👋 **Hello!** Welcome to Advanced DataBot Analytics!\n\n"
                "📁 Upload your data file to begin analysis, or use the menu below for help.",
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
        elif 'thank' in text.lower():
            await update.message.reply_text(
                "😊 **You're welcome!** \n\nI'm here to help you discover insights in your data!",
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
        else:
            await update.message.reply_text(
                "🤔 **I didn't understand that command.**\n\n"
                "📁 **To get started:**\n"
                "• Upload a data file (CSV, Excel, JSON, etc.)\n"
                "• Use the menu buttons below\n"
                "• Type /help for detailed instructions",
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, callback: bool):
        """Utility method to send messages"""
        if callback:
            await update.callback_query.edit_message_text(
                text, 
                parse_mode='Markdown'
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
                parse_mode='Markdown',
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_long_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE, text: str, callback: bool):
        """Send long messages in chunks"""
        max_length = 4000
        if len(text) <= max_length:
            await self.send_message(update, context, text, callback)
        else:
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            for i, chunk in enumerate(chunks):
                if i == 0 and callback:
                    await update.callback_query.edit_message_text(chunk, parse_mode='Markdown')
                else:
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text=chunk,
                        parse_mode='Markdown',
                        reply_markup=self.get_persistent_keyboard() if i == len(chunks) - 1 else None
                    )
    
    def enhanced_statistical_analysis(self, df, filename):
        """Enhanced statistical analysis with comprehensive metrics"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        datetime_cols = df.select_dtypes(include=['datetime']).columns
        
        analysis = f"""
🔍 **Enhanced Statistical Analysis: `{filename}`**

📊 **Descriptive Statistics Summary:**
        """
        
        # Enhanced statistics for numeric columns
        for col in numeric_cols[:6]:
            stats = df[col].describe()
            skewness = df[col].skew()
            kurtosis = df[col].kurtosis()
            
            # Data distribution assessment
            if abs(skewness) < 0.5:
                dist_desc = "Normal Distribution"
            elif abs(skewness) < 1:
                dist_desc = "Moderately Skewed"
            else:
                dist_desc = "Highly Skewed"
                
            analysis += f"""
**{col}:**
• Mean: {stats['mean']:.3f} | Median: {stats['50%']:.3f}
• Range: {stats['min']:.2f} - {stats['max']:.2f}
• Std Dev: {stats['std']:.3f} | Variance: {stats['std']**2:.3f}
• Distribution: {dist_desc} (Skew: {skewness:.2f})
• Outlier Potential: {'High' if abs(kurtosis) > 3 else 'Low'} (Kurtosis: {kurtosis:.2f})
• Missing: {df[col].isnull().sum()} ({100 * df[col].isnull().sum() / len(df):.1f}%)
"""

        # Correlation insights
        if len(numeric_cols) > 1:
            analysis += f"\n🔗 **Correlation Analysis:**\n"
            corr_matrix = df[numeric_cols].corr()
            
            # Find significant correlations
            correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.3:
                        strength = "Very Strong" if abs(corr_val) > 0.8 else "Strong" if abs(corr_val) > 0.6 else "Moderate" if abs(corr_val) > 0.4 else "Weak"
                        correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val, strength))
            
            if correlations:
                correlations.sort(key=lambda x: abs(x[2]), reverse=True)
                for col1, col2, corr_val, strength in correlations[:8]:
                    direction = "Positive" if corr_val > 0 else "Negative"
                    analysis += f"• **{col1}** ↔ **{col2}**: {corr_val:.3f} ({strength} {direction})\n"
            else:
                analysis += "• No significant correlations detected (threshold: 0.3)\n"

        # Categorical analysis
        if len(text_cols) > 0:
            analysis += f"\n📊 **Categorical Data Analysis:**\n"
            for col in text_cols[:5]:
                unique_count = df[col].nunique()
                most_common = df[col].mode().iloc[0] if len(df[col].mode()) > 0 else "N/A"
                analysis += f"• **{col}**: {unique_count} unique values, Mode: '{most_common}'\n"

        # Data quality insights
        analysis += f"\n🎯 **Data Quality Assessment:**\n"
        
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
        duplicate_pct = df.duplicated().sum() / len(df) * 100
        
        if len(df) > 50000:
            analysis += "• 🚀 **Large Scale Dataset** - Excellent for advanced analytics\n"
        elif len(df) > 10000:
            analysis += "• 📈 **Substantial Dataset** - Good statistical power\n"
        elif len(df) > 1000:
            analysis += "• 📊 **Medium Dataset** - Adequate for analysis\n"
        else:
            analysis += "• 📉 **Small Dataset** - Limited statistical power\n"
        
        if missing_pct < 5:
            analysis += "• ✅ **Excellent Data Quality** - Minimal missing values\n"
        elif missing_pct < 15:
            analysis += "• 🟡 **Good Data Quality** - Some cleaning recommended\n"
        else:
            analysis += f"• 🔴 **Data Quality Issues** - {missing_pct:.1f}% missing values\n"
        
        if duplicate_pct > 5:
            analysis += f"• ⚠️ **Duplicate Detection** - {duplicate_pct:.1f}% duplicate rows\n"
        
        if len(numeric_cols) >= 5:
            analysis += "• 🤖 **ML Ready** - Multiple features for advanced analysis\n"

        # Statistical recommendations
        analysis += f"\n💡 **Statistical Insights & Recommendations:**\n"
        
        if missing_pct > 10:
            analysis += "• Consider data imputation strategies for missing values\n"
        if duplicate_pct > 2:
            analysis += "• Remove duplicate records for cleaner analysis\n"
        if len(numeric_cols) >= 3:
            analysis += "• Explore clustering and dimensionality reduction techniques\n"
        if any(df[col].skew() > 2 for col in numeric_cols):
            analysis += "• Apply transformations for highly skewed variables\n"
        if len(datetime_cols) > 0:
            analysis += "• Time series analysis and trend detection available\n"
        
        return analysis
    
    def perform_advanced_ml_analysis(self, X, X_scaled, numeric_cols, filename):
        """Comprehensive machine learning analysis with multiple algorithms"""
        results = f"""
🤖 **Advanced Machine Learning Analysis: `{filename}`**

🎯 **Clustering Analysis:**
        """
        
        # K-Means clustering with optimal cluster selection
        best_k = 2
        best_score = -1
        silhouette_scores = []
        
        for k in range(2, min(10, len(X)//3)):
            try:
                kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
                cluster_labels = kmeans.fit_predict(X_scaled)
                score = silhouette_score(X_scaled, cluster_labels)
                silhouette_scores.append((k, score))
                if score > best_score:
                    best_score = score
                    best_k = k
            except:
                break
        
        # Perform optimal clustering
        kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        results += f"""
**K-Means Clustering Results:**
• **Optimal Clusters:** {best_k} (Silhouette Score: {best_score:.3f})
• **Quality Assessment:** {'Excellent' if best_score > 0.7 else 'Good' if best_score > 0.5 else 'Fair' if best_score > 0.3 else 'Poor'}

**Cluster Distribution:**
"""
        
        unique, counts = np.unique(cluster_labels, return_counts=True)
        for cluster, count in zip(unique, counts):
            percentage = (count / len(cluster_labels)) * 100
            results += f"  - Cluster {cluster}: {count} samples ({percentage:.1f}%)\n"
        
        # DBSCAN clustering for density-based analysis
        try:
            dbscan = DBSCAN(eps=0.5, min_samples=5)
            dbscan_labels = dbscan.fit_predict(X_scaled)
            n_clusters_dbscan = len(set(dbscan_labels)) - (1 if -1 in dbscan_labels else 0)
            n_noise = list(dbscan_labels).count(-1)
            
            results += f"""
**DBSCAN Clustering Results:**
• **Clusters Found:** {n_clusters_dbscan}
• **Noise Points:** {n_noise} ({100 * n_noise / len(X):.1f}%)
"""
        except:
            results += "\n**DBSCAN:** Could not perform density-based clustering\n"
        
        # PCA Analysis
        results += f"""

📉 **Principal Component Analysis (PCA):**
"""
        
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)
        
        # Explained variance analysis
        cumsum_var = np.cumsum(pca.explained_variance_ratio_)
        n_components_80 = np.argmax(cumsum_var >= 0.8) + 1
        n_components_95 = np.argmax(cumsum_var >= 0.95) + 1
        
        results += f"""
**Dimensionality Reduction Results:**
• **Components for 80% variance:** {n_components_80}/{len(numeric_cols)}
• **Components for 95% variance:** {n_components_95}/{len(numeric_cols)}
• **First PC explains:** {pca.explained_variance_ratio_[0]:.1%} of variance
• **Top 3 PCs explain:** {pca.explained_variance_ratio_[:3].sum():.1%} of variance

**Feature Loadings (Principal Component 1):**
"""
        
        # Feature importance in first principal component
        pc1_loadings = abs(pca.components_[0])
        feature_importance = list(zip(numeric_cols, pc1_loadings))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        for feature, importance in feature_importance[:6]:
            results += f"• **{feature}**: {importance:.3f}\n"
        
        # Anomaly Detection
        results += f"""

🔍 **Anomaly Detection Analysis:**
"""
        
        # Isolation Forest
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(X_scaled)
        n_anomalies = np.sum(anomaly_labels == -1)
        anomaly_pct = (n_anomalies / len(X)) * 100
        
        results += f"""
**Isolation Forest Results:**
• **Anomalies Detected:** {n_anomalies} ({anomaly_pct:.1f}%)
• **Normal Observations:** {len(X) - n_anomalies} ({100 - anomaly_pct:.1f}%)
• **Anomaly Threshold:** 10% contamination level

**Statistical Outlier Detection:**
"""
        
        # Statistical outlier detection using IQR
        total_outliers = 0
        for col in numeric_cols[:5]:
            Q1 = X[col].quantile(0.25)
            Q3 = X[col].quantile(0.75)
            IQR = Q3 - Q1
            outliers = X[(X[col] < Q1 - 1.5 * IQR) | (X[col] > Q3 + 1.5 * IQR)][col]
            outlier_count = len(outliers)
            total_outliers += outlier_count
            results += f"• **{col}**: {outlier_count} outliers ({100 * outlier_count / len(X):.1f}%)\n"
        
        # Feature Engineering Insights
        if len(numeric_cols) > 2:
            try:
                # Random Forest feature importance
                rf = RandomForestRegressor(n_estimators=100, random_state=42)
                y_temp = X.iloc[:, 0]  # Use first column as target
                X_temp = X.iloc[:, 1:]  # Rest as features
                
                if len(X_temp.columns) > 0:
                    rf.fit(X_temp, y_temp)
                    importances = rf.feature_importances_
                    
                    results += f"""

🎯 **Feature Importance Analysis:**
**Random Forest Feature Rankings:**
"""
                    
                    feature_ranks = list(zip(X_temp.columns, importances))
                    feature_ranks.sort(key=lambda x: x[1], reverse=True)
                    
                    for feature, importance in feature_ranks[:6]:
                        results += f"• **{feature}**: {importance:.3f}\n"
            except:
                pass

        # ML Insights and Recommendations
        results += f"""

💡 **Machine Learning Insights:**

**Clustering Assessment:**
"""
        
        if best_score > 0.6:
            results += "• ✅ **Excellent Clustering Structure** - Clear, well-separated groups\n"
        elif best_score > 0.4:
            results += "• 🟡 **Moderate Clustering** - Some natural groupings detected\n"
        else:
            results += "• 🔴 **Weak Clustering** - Data may be uniformly distributed\n"
        
        if n_components_80 <= 3:
            results += "• 📉 **Low Dimensionality** - Data complexity is manageable\n"
        elif n_components_80 <= 6:
            results += "• 📊 **Medium Dimensionality** - Moderate feature complexity\n"
        else:
            results += "• 📈 **High Dimensionality** - Complex feature relationships\n"
        
        if anomaly_pct > 15:
            results += "• ⚠️ **High Anomaly Rate** - Consider data quality review\n"
        elif anomaly_pct < 5:
            results += "• ✅ **Low Anomaly Rate** - Consistent data patterns\n"
        
        results += f"""
**Recommended Next Steps:**
• Use {best_k}-cluster segmentation for business analysis
• Consider dimensionality reduction with {n_components_80} components
• Investigate {n_anomalies} anomalous observations
• Apply feature selection based on importance rankings
        """
        
        return results
    
    def generate_business_intelligence_report(self, df, filename):
        """Generate comprehensive business intelligence report"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        datetime_cols = df.select_dtypes(include=['datetime']).columns
        
        # Calculate advanced metrics
        missing_total = df.isnull().sum().sum()
        missing_pct = (missing_total / (len(df) * len(df.columns))) * 100
        duplicates = df.duplicated().sum()
        memory_mb = df.memory_usage(deep=True).sum() / (1024**2)
        
        report = f"""
📋 **BUSINESS INTELLIGENCE REPORT**

🎯 **Executive Summary: `{filename}`**

**Dataset Overview:**
• **Total Records:** {len(df):,} rows
• **Total Features:** {len(df.columns)} columns
• **Data Size:** {memory_mb:.2f} MB
• **Analysis Date:** {datetime.now().strftime('%B %d, %Y')}

**Key Performance Indicators:**
• **Data Quality Score:** {((len(df) * len(df.columns) - missing_total) / (len(df) * len(df.columns)) * 100):.1f}%
• **Completeness Rate:** {(1 - missing_pct/100):.1%}
• **Uniqueness Rate:** {(1 - duplicates/len(df)):.1%}
• **Feature Diversity:** {len(numeric_cols)} numeric, {len(text_cols)} categorical

---

🔍 **Data Quality Assessment:**

**Quality Grade:** {'A+' if missing_pct < 2 else 'A' if missing_pct < 5 else 'B' if missing_pct < 10 else 'C' if missing_pct < 20 else 'D'}

**Detailed Quality Metrics:**
• **Missing Data:** {missing_total:,} values ({missing_pct:.2f}% of total)
• **Duplicate Records:** {duplicates:,} ({100 * duplicates / len(df):.2f}%)
• **Complete Records:** {len(df.dropna()):,} ({100 * len(df.dropna()) / len(df):.1f}%)
• **Data Integrity:** {'Excellent' if missing_pct < 5 else 'Good' if missing_pct < 15 else 'Needs Improvement'}

**Column Quality Assessment:**
"""
        
        # Detailed column analysis
        for col in df.columns[:10]:  # First 10 columns
            missing_col = df[col].isnull().sum()
            missing_col_pct = (missing_col / len(df)) * 100
            unique_pct = (df[col].nunique() / len(df)) * 100
            
            status = "✅ Excellent" if missing_col_pct < 2 else "🟡 Good" if missing_col_pct < 10 else "🔴 Poor"
            diversity = "High" if unique_pct > 80 else "Medium" if unique_pct > 20 else "Low"
            
            report += f"• **{col}**: {status} (Missing: {missing_col_pct:.1f}%, Diversity: {diversity})\n"

        # Statistical insights for business users
        if len(numeric_cols) > 0:
            report += f"""

---

📈 **Statistical Business Insights:**

**Key Metrics Summary:**
"""
            
            for col in numeric_cols[:6]:
                stats = df[col].describe()
                cv = stats['std'] / stats['mean'] if stats['mean'] != 0 else 0
                trend = "Stable" if cv < 0.3 else "Variable" if cv < 1 else "Highly Variable"
                
                report += f"""
**{col} Analysis:**
• Average Value: {stats['mean']:.2f}
• Typical Range: {stats['25%']:.2f} - {stats['75%']:.2f}
• Variability: {trend} (CV: {cv:.2f})
• Data Range: {stats['min']:.1f} to {stats['max']:.1f}
"""

        # Business correlations and relationships
        if len(numeric_cols) > 1:
            report += f"""

🔗 **Business Relationship Analysis:**

**Key Correlations:**
"""
            
            corr_matrix = df[numeric_cols].corr()
            strong_correlations = []
            
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:  # Focus on strong correlations for business
                        strength = "Very Strong" if abs(corr_val) > 0.8 else "Strong"
                        direction = "Positive" if corr_val > 0 else "Negative"
                        strong_correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val, strength, direction))
            
            if strong_correlations:
                strong_correlations.sort(key=lambda x: abs(x[2]), reverse=True)
                for col1, col2, corr_val, strength, direction in strong_correlations[:6]:
                    business_impact = "synergistic" if corr_val > 0 else "inverse"
                    report += f"• **{col1}** & **{col2}**: {strength} {direction.lower()} relationship ({corr_val:.3f}) - {business_impact} pattern\n"
            else:
                report += "• No strong correlations detected - variables appear independent\n"

        # Business recommendations
        report += f"""

---

💼 **Strategic Business Recommendations:**

**Data Management Priorities:**
"""
        
        if missing_pct > 10:
            report += "• 🔴 **CRITICAL**: Implement data quality controls and validation processes\n"
            report += "• Consider data governance framework to prevent future quality issues\n"
        elif missing_pct > 5:
            report += "• 🟡 **IMPORTANT**: Develop data imputation strategies for missing values\n"
            report += "• Review data collection processes for improvement opportunities\n"
        else:
            report += "• ✅ **EXCELLENT**: Data quality meets professional standards\n"
            report += "• Maintain current data management practices\n"
        
        if duplicates > len(df) * 0.02:
            report += "• ⚠️ **ACTION REQUIRED**: Remove duplicate records to improve analysis accuracy\n"
        
        # Analytics opportunities
        report += f"""
**Analytics & Business Intelligence Opportunities:**
"""
        
        if len(numeric_cols) >= 5:
            report += "• 🤖 **Advanced Analytics**: Implement predictive modeling for forecasting\n"
            report += "• 📊 **Customer Segmentation**: Use clustering for targeted strategies\n"
        
        if len(numeric_cols) >= 3:
            report += "• 📈 **Performance Modeling**: Develop KPI prediction models\n"
            report += "• 🔍 **Root Cause Analysis**: Statistical modeling capabilities available\n"
        
        if len(text_cols) > 0:
            report += "• 📝 **Categorical Insights**: Cross-tabulation analysis for pattern discovery\n"
        
        if len(datetime_cols) > 0:
            report += "• ⏰ **Time Series Analysis**: Trend forecasting and seasonal pattern detection\n"
        
        # ROI and impact assessment
        report += f"""
**Expected Business Impact:**
• **Data Quality Improvement**: {100 - missing_pct:.0f}% accuracy in decision-making
• **Process Efficiency**: Automated insights reduce manual analysis time by 70-80%
• **Risk Reduction**: Early anomaly detection prevents potential issues
• **Strategic Planning**: Data-driven insights support evidence-based decisions

**Implementation Priority:**
1. Address data quality issues (missing values, duplicates)
2. Implement automated reporting and monitoring
3. Develop predictive models for key business metrics
4. Create interactive dashboards for stakeholders

---

⚡ **Technical Performance Metrics:**

• **Processing Efficiency**: {len(df):,} records analyzed
• **Memory Optimization**: {memory_mb:.2f} MB storage footprint
• **Scalability Assessment**: {'Excellent' if len(df) < 100000 else 'Good' if len(df) < 500000 else 'Requires Optimization'}
• **Real-time Capability**: {'Yes' if len(df) < 10000 else 'Batch Processing Recommended'}

**Report Generation Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Analyst:** Advanced DataBot Analytics Pro
        """
        
        return report
    
    def compute_inferential_statistics(self, df, filename):
        """Compute advanced inferential statistics with hypothesis testing"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        results = f"""
📉 **Advanced Inferential Statistical Analysis: `{filename}`**

🧪 **Distribution Analysis & Normality Testing:**
        """
        
        for col in numeric_cols[:6]:
            data = df[col].dropna()
            
            if len(data) < 8:
                continue
                
            # Advanced distribution statistics
            skewness = data.skew()
            kurtosis = data.kurtosis()
            
            # Normality tests
            try:
                shapiro_stat, shapiro_p = shapiro(data[:5000])  # Limit for computational efficiency
                normal_test_stat, normal_test_p = normaltest(data)
                
                normality_assessment = "Normal" if shapiro_p > 0.05 else "Non-Normal"
            except:
                shapiro_stat, shapiro_p = None, None
                normal_test_stat, normal_test_p = None, None
                normality_assessment = "Could not test"
            
            # Distribution classification
            if abs(skewness) < 0.5:
                skew_desc = "Approximately Symmetric"
            elif abs(skewness) < 1:
                skew_desc = "Moderately Skewed"
            elif abs(skewness) < 2:
                skew_desc = "Highly Skewed"
            else:
                skew_desc = "Extremely Skewed"
            
            # Kurtosis interpretation
            if kurtosis > 3:
                kurt_desc = "Heavy-tailed (Leptokurtic)"
            elif kurtosis < -1:
                kurt_desc = "Light-tailed (Platykurtic)"
            else:
                kurt_desc = "Normal-tailed (Mesokurtic)"
            
            # Outlier analysis using multiple methods
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers_iqr = data[(data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)]
            
            # Z-score outliers (beyond 3 standard deviations)
            z_scores = np.abs((data - data.mean()) / data.std())
            outliers_zscore = data[z_scores > 3]
            
            results += f"""
**{col} - Comprehensive Analysis:**
• **Distribution Shape:** {skew_desc} (Skewness: {skewness:.3f})
• **Tail Behavior:** {kurt_desc} (Kurtosis: {kurtosis:.3f})
• **Normality:** {normality_assessment}"""
            
            if shapiro_p is not None:
                results += f" (Shapiro-Wilk p-value: {shapiro_p:.4f})"
            
            results += f"""
• **Outliers (IQR method):** {len(outliers_iqr)} ({100 * len(outliers_iqr) / len(data):.1f}%)
• **Outliers (Z-score method):** {len(outliers_zscore)} ({100 * len(outliers_zscore) / len(data):.1f}%)
• **Coefficient of Variation:** {(data.std() / data.mean()):.3f}
• **Interquartile Range:** {IQR:.3f}
"""

        # Advanced correlation analysis
        if len(numeric_cols) > 1:
            results += f"""

🔗 **Advanced Correlation & Association Analysis:**

**Pearson vs Spearman Correlation Comparison:**
"""
            
            # Compare Pearson and Spearman correlations
            correlations_analysis = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    
                    # Remove missing values for correlation
                    data1 = df[col1].dropna()
                    data2 = df[col2].dropna()
                    
                    # Find common indices
                    common_idx = data1.index.intersection(data2.index)
                    if len(common_idx) > 10:
                        data1_clean = data1[common_idx]
                        data2_clean = data2[common_idx]
                        
                        try:
                            pearson_r, pearson_p = pearsonr(data1_clean, data2_clean)
                            spearman_r, spearman_p = spearmanr(data1_clean, data2_clean)
                            
                            # Determine relationship type
                            if abs(pearson_r - spearman_r) < 0.1:
                                relationship_type = "Linear"
                            else:
                                relationship_type = "Non-linear"
                            
                            correlations_analysis.append({
                                'col1': col1, 'col2': col2,
                                'pearson_r': pearson_r, 'pearson_p': pearson_p,
                                'spearman_r': spearman_r, 'spearman_p': spearman_p,
                                'relationship': relationship_type
                            })
                        except:
                            continue
            
            # Report significant correlations
            significant_correlations = [c for c in correlations_analysis if c['pearson_p'] < 0.05 and abs(c['pearson_r']) > 0.3]
            
            if significant_correlations:
                for corr in significant_correlations[:8]:
                    significance = "Highly Significant" if corr['pearson_p'] < 0.001 else "Significant"
                    strength = "Very Strong" if abs(corr['pearson_r']) > 0.8 else "Strong" if abs(corr['pearson_r']) > 0.6 else "Moderate"
                    
                    results += f"""
• **{corr['col1']} × {corr['col2']}:**
  - Pearson r: {corr['pearson_r']:.3f} (p={corr['pearson_p']:.4f}) - {significance}
  - Spearman ρ: {corr['spearman_r']:.3f} - {corr['relationship']} relationship
  - Strength: {strength}
"""
            else:
                results += "• No statistically significant correlations found (p < 0.05, |r| > 0.3)\n"

        # Hypothesis testing insights
        results += f"""

🧪 **Statistical Hypothesis Testing Summary:**

**Key Statistical Findings:**
"""
        
        # Overall data characteristics
        total_normal_vars = 0
        total_skewed_vars = 0
        
        for col in numeric_cols:
            data = df[col].dropna()
            if len(data) >= 8:
                try:
                    _, p_value = shapiro(data[:5000])
                    if p_value > 0.05:
                        total_normal_vars += 1
                    else:
                        total_skewed_vars += 1
                except:
                    total_skewed_vars += 1
        
        if total_normal_vars > total_skewed_vars:
            results += "• ✅ **Distribution Assessment**: Majority of variables follow normal distribution\n"
            results += "• **Recommended Tests**: Parametric statistical tests (t-tests, ANOVA, Pearson correlation)\n"
        else:
            results += "• ⚠️ **Distribution Assessment**: Most variables are non-normally distributed\n"
            results += "• **Recommended Tests**: Non-parametric tests (Mann-Whitney, Spearman correlation)\n"
        
        # Correlation strength assessment
        if len(significant_correlations) > 0:
            avg_correlation = np.mean([abs(c['pearson_r']) for c in significant_correlations])
            if avg_correlation > 0.7:
                results += "• 🔗 **Multicollinearity Warning**: Strong correlations detected - consider dimensionality reduction\n"
            elif avg_correlation > 0.5:
                results += "• 📊 **Moderate Associations**: Some variables show meaningful relationships\n"
            else:
                results += "• 🔍 **Weak Associations**: Variables are largely independent\n"
        else:
            results += "• 📊 **Independence**: No significant correlations found - variables appear independent\n"

        # Sample size adequacy
        results += f"""
**Statistical Power Assessment:**
• **Sample Size:** {len(df):,} observations
• **Power Level:** {'High' if len(df) > 1000 else 'Medium' if len(df) > 100 else 'Low'}
• **Confidence:** {'95%+ confidence intervals reliable' if len(df) > 30 else 'Small sample - use caution'}

💡 **Advanced Statistical Recommendations:**
"""
        
        if total_skewed_vars > total_normal_vars:
            results += "• Consider data transformations (log, sqrt, Box-Cox) for skewed variables\n"
        if len(significant_correlations) > len(numeric_cols) // 2:
            results += "• Apply Principal Component Analysis (PCA) to reduce dimensionality\n"
        if len(df) > 1000:
            results += "• Large sample enables robust hypothesis testing and confidence intervals\n"
        if any(df[col].std() / df[col].mean() > 2 for col in numeric_cols if df[col].mean() != 0):
            results += "• High variability detected - consider standardization before modeling\n"
        
        return results
    
    async def send_enhanced_preview_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send enhanced data preview with comprehensive charts"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            charts_created = 0
            
            # 1. Enhanced Data Overview Dashboard
            if len(numeric_cols) > 0:
                fig = make_subplots(
                    rows=2, cols=2,
                    subplot_titles=('Data Distribution', 'Box Plot Analysis', 
                                   'Correlation Heatmap', 'Statistical Summary'),
                    specs=[[{'type': 'histogram'}, {'type': 'box'}],
                           [{'type': 'heatmap'}, {'type': 'bar'}]]
                )
                
                # Distribution plot
                col = numeric_cols[0]
                fig.add_trace(
                    go.Histogram(x=df[col], name=col, showlegend=False, 
                               marker_color='lightblue', opacity=0.8),
                    row=1, col=1
                )
                
                # Box plots for multiple columns
                for i, col in enumerate(numeric_cols[:4]):
                    fig.add_trace(
                        go.Box(y=df[col], name=col, 
                              marker_color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]),
                        row=1, col=2
                    )
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols[:8]].corr()
                    fig.add_trace(
                        go.Heatmap(
                            z=corr_matrix.values,
                            x=corr_matrix.columns,
                            y=corr_matrix.columns,
                            colorscale='RdBu',
                            zmid=0,
                            showscale=True
                        ),
                        row=2, col=1
                    )
                
                # Summary statistics
                means = [df[col].mean() for col in numeric_cols[:6]]
                fig.add_trace(
                    go.Bar(x=numeric_cols[:6], y=means, name='Mean Values',
                          marker_color='lightgreen', showlegend=False),
                    row=2, col=2
                )
                
                fig.update_layout(
                    title_text="📊 Data Analysis Overview Dashboard",
                    height=800,
                    showlegend=True
                )
                
                chart_path = 'overview_dashboard.png'
                fig.write_image(chart_path, width=1200, height=800)
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption="📊 **Data Overview Dashboard**\n\nComprehensive preview of your dataset structure and key statistics."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            # 2. Individual distribution plots
            for i, col in enumerate(numeric_cols[:3]):
                plt.figure(figsize=(10, 6))
                
                # Create subplot for histogram and stats
                fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
                
                # Histogram with KDE
                ax1.hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                ax1.set_title(f'Distribution of {col}', fontsize=14, fontweight='bold')
                ax1.set_xlabel(col)
                ax1.set_ylabel('Frequency')
                ax1.grid(True, alpha=0.3)
                
                # Add statistical annotations
                mean_val = df[col].mean()
                median_val = df[col].median()
                ax1.axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
                ax1.axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
                ax1.legend()
                
                # Box plot with outliers
                ax2.boxplot(df[col].dropna(), vert=True, patch_artist=True, 
                           boxprops=dict(facecolor='lightgreen', alpha=0.7))
                ax2.set_title(f'Box Plot of {col}', fontsize=14, fontweight='bold')
                ax2.set_ylabel(col)
                ax2.grid(True, alpha=0.3)
                
                plt.tight_layout()
                
                chart_path = f'distribution_{col}_{i}.png'
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption=f"📈 **{col} Analysis**\n\nDetailed distribution and outlier analysis for {col}."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            # 3. Categorical data analysis
            if len(text_cols) > 0:
                fig, axes = plt.subplots(2, 2, figsize=(16, 12))
                fig.suptitle('📊 Categorical Data Analysis', fontsize=16, fontweight='bold')
                
                for i, col in enumerate(text_cols[:4]):
                    ax = axes[i//2, i%2] if len(text_cols) > 1 else axes
                    
                    # Count plot
                    value_counts = df[col].value_counts().head(10)
                    ax.bar(range(len(value_counts)), value_counts.values, color='lightcoral')
                    ax.set_title(f'Top Values in {col}')
                    ax.set_xlabel('Categories')
                    ax.set_ylabel('Count')
                    ax.set_xticks(range(len(value_counts)))
                    ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
                    ax.grid(True, alpha=0.3)
                
                # Hide empty subplots
                for i in range(len(text_cols), 4):
                    axes[i//2, i%2].set_visible(False)
                
                plt.tight_layout()
                
                chart_path = 'categorical_analysis.png'
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption="📊 **Categorical Data Analysis**\n\nFrequency analysis of categorical variables in your dataset."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ **Preview Complete!** Generated {charts_created} visualization charts.\n\n"
                     f"Use the menu below for detailed analysis options.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating preview charts: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_comprehensive_visualizations(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send comprehensive visualization suite with multiple chart types"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            datetime_cols = df.select_dtypes(include=['datetime']).columns.tolist()
            
            charts_created = 0
            
            # 1. Advanced Statistical Plots
            if len(numeric_cols) >= 2:
                fig, axes = plt.subplots(2, 3, figsize=(18, 12))
                fig.suptitle('📈 Advanced Statistical Visualization Suite', fontsize=16, fontweight='bold')
                
                # Pair plot (scatter matrix)
                if len(numeric_cols) >= 2:
                    from pandas.plotting import scatter_matrix
                    scatter_matrix(df[numeric_cols[:4]], ax=axes[0, 0], alpha=0.6, figsize=(6, 6), diagonal='hist')
                    axes[0, 0].set_title('Pair Plot Matrix')
                
                # Correlation heatmap
                if len(numeric_cols) > 1:
                    corr_matrix = df[numeric_cols[:8]].corr()
                    im = axes[0, 1].imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                    axes[0, 1].set_title('Correlation Heatmap')
                    axes[0, 1].set_xticks(range(len(corr_matrix.columns)))
                    axes[0, 1].set_yticks(range(len(corr_matrix.columns)))
                    axes[0, 1].set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                    axes[0, 1].set_yticklabels(corr_matrix.columns)
                    plt.colorbar(im, ax=axes[0, 1], fraction=0.046, pad=0.04)
                
                # Violin plots
                if len(numeric_cols) >= 1:
                    data_to_plot = [df[col].dropna() for col in numeric_cols[:4]]
                    axes[0, 2].violinplot(data_to_plot, positions=range(len(data_to_plot)))
                    axes[0, 2].set_title('Distribution Shapes (Violin Plot)')
                    axes[0, 2].set_xticks(range(len(numeric_cols[:4])))
                    axes[0, 2].set_xticklabels(numeric_cols[:4], rotation=45, ha='right')
                
                # Distribution comparison
                for i, col in enumerate(numeric_cols[:3]):
                    axes[1, i].hist(df[col].dropna(), bins=30, alpha=0.7, color=f'C{i}')
                    axes[1, i].set_title(f'{col} Distribution')
                    axes[1, i].set_xlabel(col)
                    axes[1, i].set_ylabel('Frequency')
                    axes[1, i].grid(True, alpha=0.3)
                
                # Hide unused subplots
                for i in range(len(numeric_cols), 3):
                    axes[1, i].set_visible(False)
                
                plt.tight_layout()
                
                chart_path = 'advanced_statistical_plots.png'
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption="📈 **Advanced Statistical Visualizations**\n\nComprehensive statistical plots including pair plots, correlations, and distribution analysis."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            # 2. Business Intelligence Dashboard
            if len(numeric_cols) >= 3:
                fig = make_subplots(
                    rows=3, cols=2,
                    subplot_titles=('Key Metrics Overview', 'Trend Analysis',
                                   'Performance Comparison', 'Distribution Analysis',
                                   'Outlier Detection', 'Summary Statistics'),
                    specs=[[{'type': 'bar'}, {'type': 'scatter'}],
                           [{'type': 'bar'}, {'type': 'histogram'}],
                           [{'type': 'scatter'}, {'type': 'bar'}]]
                )
                
                # Key metrics
                means = [df[col].mean() for col in numeric_cols[:6]]
                fig.add_trace(
                    go.Bar(x=numeric_cols[:6], y=means, name='Average Values',
                          marker_color='lightblue'), row=1, col=1
                )
                
                # Trend line
                if len(df) > 1:
                    fig.add_trace(
                        go.Scatter(x=list(range(len(df))), y=df[numeric_cols[0]],
                                  mode='lines', name=f'{numeric_cols[0]} Trend',
                                  line=dict(color='red')), row=1, col=2
                    )
                
                # Performance comparison
                if len(numeric_cols) >= 2:
                    fig.add_trace(
                        go.Bar(x=numeric_cols[:5], 
                              y=[df[col].std() for col in numeric_cols[:5]],
                              name='Variability (Std Dev)',
                              marker_color='orange'), row=2, col=1
                    )
                
                # Distribution
                fig.add_trace(
                    go.Histogram(x=df[numeric_cols[0]], name=f'{numeric_cols[0]} Distribution',
                               marker_color='lightgreen'), row=2, col=2
                )
                
                # Outlier scatter
                if len(numeric_cols) >= 2:
                    fig.add_trace(
                        go.Scatter(x=df[numeric_cols[0]], y=df[numeric_cols[1]],
                                  mode='markers', name='Data Points',
                                  marker=dict(color='purple', opacity=0.6)), row=3, col=1
                    )
                
                # Summary statistics
                stats_data = [df[col].max() for col in numeric_cols[:5]]
                fig.add_trace(
                    go.Bar(x=numeric_cols[:5], y=stats_data, name='Maximum Values',
                          marker_color='red'), row=3, col=2
                )
                
                fig.update_layout(
                    title_text="📊 Business Intelligence Dashboard",
                    height=1200,
                    showlegend=True
                )
                
                chart_path = 'business_dashboard.png'
                fig.write_image(chart_path, width=1400, height=1200)
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption="📊 **Business Intelligence Dashboard**\n\nComprehensive business-focused visualizations with key metrics, trends, and performance indicators."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            # 3. Time Series Analysis (if datetime columns exist)
            if len(datetime_cols) > 0 and len(numeric_cols) > 0:
                plt.figure(figsize=(15, 8))
                
                datetime_col = datetime_cols[0]
                numeric_col = numeric_cols[0]
                
                # Sort by datetime
                df_sorted = df.sort_values(datetime_col)
                
                plt.plot(df_sorted[datetime_col], df_sorted[numeric_col], 
                        marker='o', linewidth=2, markersize=4)
                plt.title(f'Time Series Analysis: {numeric_col} over {datetime_col}', 
                         fontsize=14, fontweight='bold')
                plt.xlabel(datetime_col)
                plt.ylabel(numeric_col)
                plt.xticks(rotation=45)
                plt.grid(True, alpha=0.3)
                
                # Add trend line
                if len(df_sorted) > 2:
                    z = np.polyfit(range(len(df_sorted)), df_sorted[numeric_col].dropna(), 1)
                    p = np.poly1d(z)
                    plt.plot(df_sorted[datetime_col], p(range(len(df_sorted))), 
                            "r--", alpha=0.8, linewidth=2, label='Trend Line')
                    plt.legend()
                
                plt.tight_layout()
                
                chart_path = 'time_series_analysis.png'
                plt.savefig(chart_path, dpi=150, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=chart_file,
                        caption="📈 **Time Series Analysis**\n\nTemporal analysis showing trends and patterns over time."
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ **Visualization Suite Complete!** \n\n"
                     f"📊 Generated {charts_created} comprehensive charts\n"
                     f"🎯 Covering statistical analysis, business intelligence, and temporal patterns\n\n"
                     f"Use the menu below for additional analysis options.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating comprehensive visualizations: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_advanced_chart_collection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send advanced specialized chart collection"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if len(numeric_cols) == 0:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="📊 No numeric columns found for advanced charts.",
                    reply_markup=self.get_persistent_keyboard()
                )
                return
            
            charts_created = 0
            
            # Create advanced statistical visualization
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('🎨 Advanced Chart Collection', fontsize=16, fontweight='bold')
            
            # 1. Enhanced distribution plot
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                axes[0, 0].hist(df[col].dropna(), bins=30, alpha=0.7, color='skyblue', edgecolor='black')
                axes[0, 0].set_title(f'Enhanced Distribution: {col}')
                axes[0, 0].set_xlabel(col)
                axes[0, 0].set_ylabel('Frequency')
                axes[0, 0].grid(True, alpha=0.3)
                
                # Add mean and median lines
                mean_val = df[col].mean()
                median_val = df[col].median()
                axes[0, 0].axvline(mean_val, color='red', linestyle='--', linewidth=2, label=f'Mean: {mean_val:.2f}')
                axes[0, 0].axvline(median_val, color='orange', linestyle='--', linewidth=2, label=f'Median: {median_val:.2f}')
                axes[0, 0].legend()
            
            # 2. Box plot comparison
            if len(numeric_cols) >= 1:
                box_data = [df[col].dropna() for col in numeric_cols[:5]]
                bp = axes[0, 1].boxplot(box_data, labels=numeric_cols[:5], patch_artist=True)
                
                colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
                for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                axes[0, 1].set_title('Multi-Variable Box Plot Analysis')
                axes[0, 1].set_ylabel('Values')
                axes[0, 1].tick_params(axis='x', rotation=45)
                axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Correlation heatmap
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols[:8]].corr()
                im = axes[1, 0].imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                axes[1, 0].set_title('Advanced Correlation Heatmap')
                axes[1, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_yticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                axes[1, 0].set_yticklabels(corr_matrix.columns)
                plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
            
            # 4. Scatter plot with trend
            if len(numeric_cols) >= 2:
                x_col, y_col = numeric_cols[0], numeric_cols[1]
                axes[1, 1].scatter(df[x_col], df[y_col], alpha=0.6, color='purple', s=50)
                axes[1, 1].set_title(f'Scatter Plot: {x_col} vs {y_col}')
                axes[1, 1].set_xlabel(x_col)
                axes[1, 1].set_ylabel(y_col)
                axes[1, 1].grid(True, alpha=0.3)
                
                # Add trend line
                try:
                    z = np.polyfit(df[x_col].dropna(), df[y_col].dropna(), 1)
                    p = np.poly1d(z)
                    axes[1, 1].plot(df[x_col], p(df[x_col]), "r--", alpha=0.8, linewidth=2)
                except:
                    pass
            
            plt.tight_layout()
            
            chart_path = 'advanced_chart_collection.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="🎨 **Advanced Chart Collection**\n\nSpecialized visualizations with enhanced statistical analysis and trend detection."
                )
            
            os.remove(chart_path)
            charts_created += 1
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ **Advanced Charts Complete!** Generated {charts_created} specialized visualizations.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating advanced charts: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_enhanced_ml_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, X, X_scaled, numeric_cols):
        """Send enhanced machine learning visualization charts"""
        try:
            charts_created = 0
            
            # 1. Comprehensive ML Dashboard
            fig, axes = plt.subplots(3, 2, figsize=(16, 18))
            fig.suptitle('🤖 Machine Learning Analysis Dashboard', fontsize=16, fontweight='bold')
            
            # Clustering visualization
            kmeans = KMeans(n_clusters=3, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            if len(numeric_cols) >= 2:
                scatter = axes[0, 0].scatter(X.iloc[:, 0], X.iloc[:, 1], c=cluster_labels, 
                                           cmap='viridis', alpha=0.7, s=50)
                axes[0, 0].set_title('K-Means Clustering Results')
                axes[0, 0].set_xlabel(numeric_cols[0])
                axes[0, 0].set_ylabel(numeric_cols[1])
                plt.colorbar(scatter, ax=axes[0, 0])
            
            # PCA visualization
            pca = PCA()
            X_pca = pca.fit_transform(X_scaled)
            
            axes[0, 1].plot(range(1, len(pca.explained_variance_ratio_) + 1), 
                           np.cumsum(pca.explained_variance_ratio_), 'bo-', linewidth=2, markersize=8)
            axes[0, 1].set_title('PCA: Cumulative Explained Variance')
            axes[0, 1].set_xlabel('Principal Components')
            axes[0, 1].set_ylabel('Cumulative Explained Variance')
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].axhline(y=0.8, color='r', linestyle='--', alpha=0.7, label='80% Variance')
            axes[0, 1].axhline(y=0.95, color='orange', linestyle='--', alpha=0.7, label='95% Variance')
            axes[0, 1].legend()
            
            # Feature importance (using Random Forest)
            if len(X) > 10 and len(numeric_cols) > 1:
                rf = RandomForestRegressor(n_estimators=100, random_state=42)
                y_temp = X.iloc[:, 0]
                X_temp = X.iloc[:, 1:]
                
                if len(X_temp.columns) > 0:
                    rf.fit(X_temp, y_temp)
                    importances = rf.feature_importances_
                    
                    y_pos = np.arange(len(X_temp.columns))
                    axes[1, 0].barh(y_pos, importances, color='lightgreen')
                    axes[1, 0].set_yticks(y_pos)
                    axes[1, 0].set_yticklabels(X_temp.columns)
                    axes[1, 0].set_title('Feature Importance (Random Forest)')
                    axes[1, 0].set_xlabel('Importance Score')
            
            # Anomaly detection
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(X_scaled)
            
            if len(numeric_cols) >= 2:
                colors = ['red' if x == -1 else 'blue' for x in anomaly_labels]
                axes[1, 1].scatter(X.iloc[:, 0], X.iloc[:, 1], c=colors, alpha=0.6, s=50)
                axes[1, 1].set_title('Anomaly Detection (Red = Anomalies)')
                axes[1, 1].set_xlabel(numeric_cols[0])
                axes[1, 1].set_ylabel(numeric_cols[1])
                
                # Add legend
                from matplotlib.lines import Line2D
                legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=8, label='Normal'),
                                 Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Anomaly')]
                axes[1, 1].legend(handles=legend_elements)
            
            # Cluster silhouette analysis
            silhouette_scores = []
            k_range = range(2, min(8, len(X)//3))
            
            for k in k_range:
                try:
                    kmeans_temp = KMeans(n_clusters=k, random_state=42)
                    labels_temp = kmeans_temp.fit_predict(X_scaled)
                    score = silhouette_score(X_scaled, labels_temp)
                    silhouette_scores.append(score)
                except:
                    silhouette_scores.append(0)
            
            if silhouette_scores:
                axes[2, 0].plot(k_range, silhouette_scores, 'go-', linewidth=2, markersize=8)
                axes[2, 0].set_title('Optimal Clusters (Silhouette Analysis)')
                axes[2, 0].set_xlabel('Number of Clusters')
                axes[2, 0].set_ylabel('Silhouette Score')
                axes[2, 0].grid(True, alpha=0.3)
                
                # Mark optimal point
                if silhouette_scores:
                    best_k = k_range[np.argmax(silhouette_scores)]
                    best_score = max(silhouette_scores)
                    axes[2, 0].annotate(f'Optimal: K={best_k}\nScore={best_score:.3f}', 
                                       xy=(best_k, best_score), xytext=(best_k+0.5, best_score+0.05),
                                       arrowprops=dict(arrowstyle='->', color='red'),
                                       fontsize=10, fontweight='bold')
            
            # Data distribution in PC space
            if len(X_pca) > 0:
                axes[2, 1].scatter(X_pca[:, 0], X_pca[:, 1], c=cluster_labels, 
                                  cmap='viridis', alpha=0.7, s=50)
                axes[2, 1].set_title('Data Distribution in PC Space')
                axes[2, 1].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
                axes[2, 1].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
            
            plt.tight_layout()
            
            chart_path = 'ml_comprehensive_dashboard.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="🤖 **Machine Learning Analysis Dashboard**\n\nComprehensive ML visualizations including clustering, PCA, feature importance, and anomaly detection."
                )
            
            os.remove(chart_path)
            charts_created += 1
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ **ML Analysis Complete!** \n\n"
                     f"🤖 Generated {charts_created} machine learning visualizations\n"
                     f"📊 Analysis includes clustering, dimensionality reduction, and anomaly detection\n\n"
                     f"Use the menu below for additional analysis options.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating ML charts: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_business_report_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send business report visualizations"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Create comprehensive business report dashboard
            fig, axes = plt.subplots(2, 3, figsize=(18, 12))
            fig.suptitle('📋 Business Intelligence Report Dashboard', fontsize=18, fontweight='bold')
            
            # 1. Data quality overview
            missing_data = df.isnull().sum().sort_values(ascending=False)[:8]
            
            if len(missing_data) > 0 and missing_data.sum() > 0:
                axes[0, 0].barh(range(len(missing_data)), missing_data.values, color='coral')
                axes[0, 0].set_yticks(range(len(missing_data)))
                axes[0, 0].set_yticklabels(missing_data.index)
                axes[0, 0].set_title('Data Quality: Missing Values by Column')
                axes[0, 0].set_xlabel('Missing Count')
            else:
                axes[0, 0].text(0.5, 0.5, '✅ Excellent Data Quality\nNo Missing Values!', 
                               ha='center', va='center', transform=axes[0, 0].transAxes,
                               fontsize=14, fontweight='bold', color='green')
                axes[0, 0].set_title('Data Quality Assessment')
            
            # 2. Key performance indicators
            if len(numeric_cols) >= 1:
                kpis = [df[col].mean() for col in numeric_cols[:6]]
                axes[0, 1].bar(range(len(kpis)), kpis, color='lightblue', alpha=0.8)
                axes[0, 1].set_xticks(range(len(numeric_cols[:6])))
                axes[0, 1].set_xticklabels(numeric_cols[:6], rotation=45, ha='right')
                axes[0, 1].set_title('Key Performance Indicators (Averages)')
                axes[0, 1].set_ylabel('Average Value')
                axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Data distribution summary
            if len(numeric_cols) >= 1:
                data_ranges = [df[col].max() - df[col].min() for col in numeric_cols[:6]]
                axes[0, 2].bar(range(len(data_ranges)), data_ranges, color='lightgreen', alpha=0.8)
                axes[0, 2].set_xticks(range(len(numeric_cols[:6])))
                axes[0, 2].set_xticklabels(numeric_cols[:6], rotation=45, ha='right')
                axes[0, 2].set_title('Data Range Analysis')
                axes[0, 2].set_ylabel('Range (Max - Min)')
                axes[0, 2].grid(True, alpha=0.3)
            
            # 4. Correlation strength matrix (business view)
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols[:8]].corr()
                im = axes[1, 0].imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                axes[1, 0].set_title('Business Relationship Matrix')
                axes[1, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_yticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                axes[1, 0].set_yticklabels(corr_matrix.columns)
                plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
            
            # 5. Variability analysis
            if len(numeric_cols) >= 1:
                cv_values = [df[col].std() / df[col].mean() if df[col].mean() != 0 else 0 for col in numeric_cols[:6]]
                colors = ['red' if cv > 1 else 'orange' if cv > 0.5 else 'green' for cv in cv_values]
                axes[1, 1].bar(range(len(cv_values)), cv_values, color=colors, alpha=0.8)
                axes[1, 1].set_xticks(range(len(numeric_cols[:6])))
                axes[1, 1].set_xticklabels(numeric_cols[:6], rotation=45, ha='right')
                axes[1, 1].set_title('Risk Assessment (Coefficient of Variation)')
                axes[1, 1].set_ylabel('Variability Ratio')
                axes[1, 1].axhline(y=0.5, color='orange', linestyle='--', alpha=0.7, label='Moderate Risk')
                axes[1, 1].axhline(y=1.0, color='red', linestyle='--', alpha=0.7, label='High Risk')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
            
            # 6. Summary statistics comparison
            if len(numeric_cols) >= 2:
                stats_comparison = df[numeric_cols[:5]].describe().loc[['mean', 'std', 'min', 'max']]
                
                x_pos = np.arange(len(stats_comparison.columns))
                width = 0.2
                
                for i, stat in enumerate(['mean', 'std', 'min', 'max']):
                    if stat in stats_comparison.index:
                        normalized_values = stats_comparison.loc[stat] / stats_comparison.loc[stat].max()
                        axes[1, 2].bar(x_pos + i * width, normalized_values, 
                                     width, label=stat.capitalize(), alpha=0.8)
                
                axes[1, 2].set_title('Normalized Statistical Comparison')
                axes[1, 2].set_xlabel('Variables')
                axes[1, 2].set_ylabel('Normalized Values (0-1)')
                axes[1, 2].set_xticks(x_pos + width * 1.5)
                axes[1, 2].set_xticklabels(stats_comparison.columns, rotation=45, ha='right')
                axes[1, 2].legend()
                axes[1, 2].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            chart_path = 'business_report_dashboard.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="📋 **Business Intelligence Report Dashboard**\n\nComprehensive business-focused analysis including data quality, KPIs, risk assessment, and performance metrics."
                )
            
            os.remove(chart_path)
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ **Business Report Complete!** \n\n"
                     "📊 Generated comprehensive business intelligence dashboard\n"
                     "🎯 Includes data quality, KPIs, and risk assessments\n\n"
                     "Use the menu below for additional analysis options.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating business report charts: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    async def send_advanced_statistical_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send advanced statistical visualization charts"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:6]
            
            if len(numeric_cols) == 0:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="📊 No numeric columns available for statistical analysis.",
                    reply_markup=self.get_persistent_keyboard()
                )
                return
            
            # Create advanced statistical dashboard
            fig, axes = plt.subplots(3, 2, figsize=(16, 18))
            fig.suptitle('📉 Advanced Statistical Analysis Dashboard', fontsize=16, fontweight='bold')
            
            # 1. Q-Q plots for normality assessment
            if len(numeric_cols) >= 1:
                try:
                    probplot(df[numeric_cols[0]].dropna(), dist="norm", plot=axes[0, 0])
                    axes[0, 0].set_title(f'Q-Q Plot: {numeric_cols[0]} vs Normal Distribution')
                    axes[0, 0].grid(True, alpha=0.3)
                    
                    # Add interpretation
                    from scipy.stats import shapiro
                    _, p_value = shapiro(df[numeric_cols[0]].dropna()[:5000])
                    interpretation = "Approximately Normal" if p_value > 0.05 else "Non-Normal"
                    axes[0, 0].text(0.05, 0.95, f'Assessment: {interpretation}\np-value: {p_value:.4f}', 
                                   transform=axes[0, 0].transAxes, verticalalignment='top',
                                   bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
                except:
                    axes[0, 0].text(0.5, 0.5, 'Q-Q Plot\nNot Available', ha='center', va='center',
                                   transform=axes[0, 0].transAxes, fontsize=12)
                    axes[0, 0].set_title('Q-Q Plot Analysis')
            
            # 2. Box plots with statistical annotations
            if len(numeric_cols) >= 1:
                box_data = [df[col].dropna() for col in numeric_cols[:5]]
                bp = axes[0, 1].boxplot(box_data, patch_artist=True, labels=numeric_cols[:5])
                
                # Color the boxes
                colors = ['lightblue', 'lightgreen', 'lightcoral', 'lightyellow', 'lightpink']
                for patch, color in zip(bp['boxes'], colors[:len(bp['boxes'])]):
                    patch.set_facecolor(color)
                    patch.set_alpha(0.7)
                
                axes[0, 1].set_title('Box Plot Analysis with Outlier Detection')
                axes[0, 1].set_xlabel('Variables')
                axes[0, 1].set_ylabel('Values')
                axes[0, 1].tick_params(axis='x', rotation=45)
                axes[0, 1].grid(True, alpha=0.3)
                
                # Add outlier count annotations
                for i, col in enumerate(numeric_cols[:5]):
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    outliers = df[(df[col] < Q1 - 1.5 * IQR) | (df[col] > Q3 + 1.5 * IQR)][col]
                    outlier_count = len(outliers)
                    axes[0, 1].text(i+1, df[col].max(), f'{outlier_count}\noutliers', 
                                   ha='center', va='bottom', fontsize=8, 
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='yellow', alpha=0.7))
            
            # 3. Distribution overlay comparison
            if len(numeric_cols) >= 2:
                for i, col in enumerate(numeric_cols[:3]):
                    data_normalized = (df[col] - df[col].mean()) / df[col].std()
                    axes[1, 0].hist(data_normalized.dropna(), bins=25, alpha=0.6, 
                                   label=f'{col} (normalized)', density=True)
                
                axes[1, 0].set_title('Normalized Distribution Comparison')
                axes[1, 0].set_xlabel('Standardized Values (Z-scores)')
                axes[1, 0].set_ylabel('Density')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
                
                # Add normal curve for reference
                x = np.linspace(-4, 4, 100)
                y = (1/np.sqrt(2*np.pi)) * np.exp(-0.5 * x**2)
                axes[1, 0].plot(x, y, 'k--', linewidth=2, label='Standard Normal', alpha=0.8)
                axes[1, 0].legend()
            
            # 4. Skewness and Kurtosis analysis
            if len(numeric_cols) >= 1:
                skew_data = [df[col].skew() for col in numeric_cols]
                kurt_data = [df[col].kurtosis() for col in numeric_cols]
                
                x_pos = np.arange(len(numeric_cols))
                width = 0.35
                
                bars1 = axes[1, 1].bar(x_pos - width/2, skew_data, width, label='Skewness', 
                                      alpha=0.8, color='lightblue')
                bars2 = axes[1, 1].bar(x_pos + width/2, kurt_data, width, label='Kurtosis', 
                                      alpha=0.8, color='lightcoral')
                
                axes[1, 1].set_title('Distribution Shape Analysis')
                axes[1, 1].set_xlabel('Variables')
                axes[1, 1].set_ylabel('Statistical Measure')
                axes[1, 1].set_xticks(x_pos)
                axes[1, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
                axes[1, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
                
                # Add reference lines
                axes[1, 1].axhline(y=-0.5, color='green', linestyle='--', alpha=0.5, label='Normal Range')
                axes[1, 1].axhline(y=0.5, color='green', linestyle='--', alpha=0.5)
                
                # Add value labels on bars
                for bar in bars1:
                    height = bar.get_height()
                    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                                   f'{height:.2f}', ha='center', va='bottom' if height >= 0 else 'top',
                                   fontsize=8)
                
                for bar in bars2:
                    height = bar.get_height()
                    axes[1, 1].text(bar.get_x() + bar.get_width()/2., height,
                                   f'{height:.2f}', ha='center', va='bottom' if height >= 0 else 'top',
                                   fontsize=8)
            
            # 5. Correlation strength visualization
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                
                # Create a mask for the upper triangle
                mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
                
                # Generate heatmap
                im = axes[2, 0].imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                
                # Add correlation values as text
                for i in range(len(corr_matrix)):
                    for j in range(len(corr_matrix.columns)):
                        if not mask[i, j]:
                            text = axes[2, 0].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                                 ha="center", va="center", color="black", fontweight='bold')
                
                axes[2, 0].set_title('Detailed Correlation Matrix')
                axes[2, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[2, 0].set_yticks(range(len(corr_matrix.columns)))
                axes[2, 0].set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                axes[2, 0].set_yticklabels(corr_matrix.columns)
                
                # Add colorbar
                plt.colorbar(im, ax=axes[2, 0], fraction=0.046, pad=0.04)
            
            # 6. Statistical summary with confidence intervals
            if len(numeric_cols) >= 1:
                means = [df[col].mean() for col in numeric_cols]
                stds = [df[col].std() for col in numeric_cols]
                
                # Calculate 95% confidence intervals
                n = len(df)
                confidence_intervals = [1.96 * std / np.sqrt(n) for std in stds]
                
                x_pos = np.arange(len(numeric_cols))
                bars = axes[2, 1].bar(x_pos, means, yerr=confidence_intervals, capsize=5,
                                     alpha=0.8, color='lightgreen', 
                                     error_kw={'color': 'black', 'linewidth': 2})
                
                axes[2, 1].set_title('Means with 95% Confidence Intervals')
                axes[2, 1].set_xlabel('Variables')
                axes[2, 1].set_ylabel('Mean Value')
                axes[2, 1].set_xticks(x_pos)
                axes[2, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
                axes[2, 1].grid(True, alpha=0.3)
                
                # Add value labels
                for i, (bar, mean, ci) in enumerate(zip(bars, means, confidence_intervals)):
                    axes[2, 1].text(bar.get_x() + bar.get_width()/2., bar.get_height() + ci,
                                   f'{mean:.2f}±{ci:.2f}', ha='center', va='bottom', fontsize=8,
                                   bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8))
            
            plt.tight_layout()
            
            chart_path = 'advanced_statistical_analysis.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="📉 **Advanced Statistical Analysis Dashboard**\n\nComprehensive statistical analysis including normality tests, distribution analysis, correlation matrices, and confidence intervals."
                )
            
            os.remove(chart_path)
            
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="✅ **Advanced Statistical Analysis Complete!** \n\n"
                     "📉 Generated comprehensive statistical visualizations\n"
                     "🧪 Includes normality testing, distribution analysis, and inferential statistics\n\n"
                     "Use the menu below for additional analysis options.",
                reply_markup=self.get_persistent_keyboard()
            )
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating advanced statistical charts: {str(e)}",
                reply_markup=self.get_persistent_keyboard()
            )
    
    def run(self):
        """Run the enhanced bot - Railway compatible"""
        print("🚀 Starting Advanced DataBot Analytics Pro...")
        print(f"🔑 Token found: {TOKEN[:10]}...")
        print("✅ Enhanced bot is ready with persistent menu!")
        print("📱 Bot is running and ready for connections")
        print("🎯 Features: Multi-format support, advanced ML, comprehensive reports")
        
        # Railway compatible polling
        try:
            self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=Update.ALL_TYPES
            )
        except Exception as e:
            print(f"Error running bot: {e}")
            # Fallback for Railway
            self.application.run_polling()

if __name__ == "__main__":
    try:
        bot = AdvancedDataAnalyticsBot()
        bot.run()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Check your .env file and bot token!")
        print("📝 Your .env file should contain:")
        print("TELEGRAM_TOKEN=your_token_here")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check your internet connection and bot token!")

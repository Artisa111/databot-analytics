#!/usr/bin/env python3
"""
========================================================================
                    DATABOT ANALYTICS PRO - TELEGRAM BOT
========================================================================

Description:
    Advanced data analysis and machine learning Telegram bot that provides
    comprehensive analytics, visualizations, and insights for CSV/Excel files.
    
Features:
    - Quick statistical analysis and data quality assessment
    - Interactive visualizations and charts
    - Machine learning analysis (clustering, PCA, anomaly detection)
    - Comprehensive reporting with business insights
    - Advanced statistical computations
    - Support for CSV and Excel files up to 50MB

Author: Artur
Quote: "Data is Love - take care of your data"

Requirements:
    - python-telegram-bot>=20.0
    - pandas, numpy, plotly, matplotlib, seaborn
    - scikit-learn, scipy
    - openpyxl, xlrd for Excel support

========================================================================
"""

import logging
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import pandas as pd
import io
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor, IsolationForest
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import warnings
warnings.filterwarnings('ignore')

# Load environment variables
load_dotenv()

# Get token
TOKEN = os.getenv('TELEGRAM_TOKEN')

# ========================================================================
#                           CONFIGURATION SETUP
# ========================================================================

# Setup logging configuration
logging.basicConfig(level=logging.INFO)

# ========================================================================
#                         MAIN BOT CLASS
# ========================================================================

class DataAnalyticsBot:
    """
    Main Telegram bot class for data analytics operations.
    
    This class handles all bot functionality including:
    - File processing and data validation
    - Statistical analysis and machine learning
    - Visualization generation
    - Report creation and insights
    """
    def __init__(self):
        if not TOKEN:
            raise ValueError("TELEGRAM_TOKEN not found in .env file!")
        
        self.application = Application.builder().token(TOKEN).build()
        self.setup_handlers()
    
    # ================================================================
    #                      BOT INITIALIZATION METHODS
    # ================================================================
    
    async def setup_bot_commands(self):
        """Setup bot commands for the menu button interface"""
        commands = [
            BotCommand("start", "🚀 Launch bot and main menu"),
            BotCommand("analyze", "📊 Quick data analysis"),
            BotCommand("visualize", "🎨 Create visualizations"),
            BotCommand("ml", "🤖 Machine learning analysis"),
            BotCommand("report", "📋 Generate full report"),
            BotCommand("stats", "📈 Advanced statistics"),
            BotCommand("help", "❓ Help and commands")
        ]
        await self.application.bot.set_my_commands(commands)
    
    
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
    
    # ================================================================
    #                      MAIN BOT COMMAND HANDLERS
    # ================================================================
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """
        Main start command handler.
        
        Sets up bot commands and displays welcome message with inline keyboard.
        This is the entry point for users to begin using the bot.
        """
        # Setup bot commands on first start
        await self.setup_bot_commands()
        
        welcome_text = """
🚀 **Welcome to DataBot Analytics Pro!**

Advanced data analysis and machine learning at your fingertips.

🎯 **What I can do:**
• 📊 Statistical Analysis & Visualizations
• 🤖 Machine Learning (Clustering, PCA, Feature Importance)
• 📈 Advanced Charts & Interactive Plots  
• 📋 Comprehensive Reports with Insights
• 🔍 Data Quality Assessment
• 💡 Actionable Recommendations

📁 **Supported Formats:** CSV, Excel (XLS/XLSX)

**💡 Use the menu button (□) next to the input field for quick access to commands!**

**Choose an option below or upload your data file to begin!**
        """
        
        # Create inline keyboard with main options
        keyboard = [
            [
                InlineKeyboardButton("📊 Quick Analysis", callback_data="quick_analyze"),
                InlineKeyboardButton("🎨 Visualizations", callback_data="create_viz")
            ],
            [
                InlineKeyboardButton("🤖 Machine Learning", callback_data="ml_analysis"),
                InlineKeyboardButton("📋 Full Report", callback_data="full_report")
            ],
            [
                InlineKeyboardButton("📈 Advanced Stats", callback_data="adv_stats"),
                InlineKeyboardButton("❓ Help & Commands", callback_data="show_help")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Send welcome message with inline buttons
        await update.message.reply_text(
            welcome_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
        
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced help command with detailed information"""
        help_text = """
🔧 **DataBot Analytics Pro - Complete Guide**

🎯 **Main Commands:**
/start - Launch interactive menu
/help - Show this comprehensive guide
/analyze - Detailed statistical analysis  
/visualize - Create quick visualizations
/charts - Generate multiple chart types
/ml - Machine learning analysis
/report - Full analytical report with insights
/stats - Advanced statistical metrics

📊 **Visualization Types:**
• Distribution plots (histograms, box plots)
• Correlation matrices & heatmaps  
• Scatter plots & pair plots
• Time series analysis
• Statistical summaries
• Outlier detection plots

🤖 **Machine Learning Features:**
• K-Means Clustering with optimization
• Principal Component Analysis (PCA)
• Feature Importance Analysis
• Anomaly Detection (Isolation Forest)
• Predictive modeling insights

📋 **Report Features:**
• Data quality assessment
• Statistical insights & trends
• Business recommendations  
• Performance metrics
• Actionable conclusions

📁 **Supported Formats:**
CSV, Excel (XLS/XLSX) - Up to 50MB

💡 **Getting Started:**
1. Send /start for interactive menu
2. Upload your data file  
3. Choose analysis type
4. Get professional insights!
        """
        
        keyboard = [
            [InlineKeyboardButton("🚀 Back to Menu", callback_data="back_to_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            help_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle callback queries from inline buttons"""
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
        elif callback_data == "show_help":
            await self.help_command(update, context)
        elif callback_data == "back_to_menu":
            await self.start(update, context)
        else:
            await query.edit_message_text("Unknown option. Please use /start to return to menu.")
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        try:
            file_name = update.message.document.file_name
            file_ext = os.path.splitext(file_name.lower())[1]
            
            # Check if file format is supported
            if file_ext not in ['.csv', '.xls', '.xlsx']:
                await update.message.reply_text(
                    "❌ **Unsupported file format!**\n"
                    "📁 Please send CSV, XLS, or XLSX files only.\n"
                    "Maximum file size: 50MB",
                    parse_mode='Markdown'
                )
                return
            
            await update.message.reply_text("📊 **Processing your file...** Please wait.")
            
            # Download file
            file = await update.message.document.get_file()
            file_bytes = await file.download_as_bytearray()
            
            # Load data based on file type
            if file_ext == '.csv':
                df = pd.read_csv(io.BytesIO(file_bytes))
            else:  # Excel files
                df = pd.read_excel(io.BytesIO(file_bytes))
            
            # Save in user context
            context.user_data['dataframe'] = df
            context.user_data['filename'] = file_name
            
            # Quick analysis
            analysis_text = self.quick_analysis(df, file_name)
            
            # Create action buttons after file upload
            keyboard = [
                [
                    InlineKeyboardButton("📊 Quick Analysis", callback_data="quick_analyze"),
                    InlineKeyboardButton("📈 Visualize", callback_data="create_viz")
                ],
                [
                    InlineKeyboardButton("🤖 ML Analysis", callback_data="ml_analysis"),
                    InlineKeyboardButton("📋 Full Report", callback_data="full_report")
                ],
                [
                    InlineKeyboardButton("📉 Advanced Stats", callback_data="adv_stats")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                analysis_text, 
                parse_mode='Markdown',
                reply_markup=reply_markup
            )
            
            # Auto-generate preview visualization
            await update.message.reply_text("🎨 **Generating preview visualization...**")
            await self.send_basic_charts(update, context, df)
            
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing file: {str(e)}")
    
    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Enhanced detailed data analysis"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "🔍 **Performing comprehensive analysis...** This may take a moment."
            if callback:
                await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(progress_text, parse_mode='Markdown')
            
            # Enhanced detailed analysis
            detailed_analysis = self.enhanced_detailed_analysis(df, filename)
            
            # Send analysis in chunks if too long
            if len(detailed_analysis) > 4000:
                chunks = [detailed_analysis[i:i+4000] for i in range(0, len(detailed_analysis), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == 0 and callback:
                        await update.callback_query.edit_message_text(chunk, parse_mode='Markdown')
                    else:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=chunk,
                            parse_mode='Markdown'
                        )
            else:
                if callback:
                    await update.callback_query.edit_message_text(detailed_analysis, parse_mode='Markdown')
                else:
                    await update.message.reply_text(detailed_analysis, parse_mode='Markdown')
            
        except Exception as e:
            error_msg = f"❌ **Analysis Error:** {str(e)}"
            if callback:
                await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def visualize(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Create enhanced visualizations"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        progress_text = "📈 **Creating advanced visualizations...** Please wait."
        
        if callback:
            await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(progress_text, parse_mode='Markdown')
            
        await self.send_enhanced_charts(update, context, df)
    
    async def create_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Generate comprehensive chart suite"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        progress_text = "🎨 **Generating comprehensive chart suite...** This will take a moment."
        
        if callback:
            await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
        else:
            await update.message.reply_text(progress_text, parse_mode='Markdown')
            
        await self.send_advanced_charts(update, context, df)
    
    async def machine_learning(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Comprehensive machine learning analysis"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "🤖 **Running ML analysis...** Computing clusters, PCA & feature importance."
            if callback:
                await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(progress_text, parse_mode='Markdown')
            
            # Get numeric columns
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) < 2:
                error_msg = "❌ **Insufficient numeric data!**\nNeed at least 2 numeric columns for ML analysis."
                if callback:
                    await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
                else:
                    await update.message.reply_text(error_msg, parse_mode='Markdown')
                return
            
            # Prepare data
            X = df[numeric_cols].dropna()
            
            if len(X) < 10:
                error_msg = "❌ **Insufficient data!**\nNeed at least 10 rows for reliable ML analysis."
                if callback:
                    await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
                else:
                    await update.message.reply_text(error_msg, parse_mode='Markdown')
                return
                
            # Standardize data
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            # Machine Learning Results
            ml_results = self.perform_ml_analysis(X, X_scaled, numeric_cols, filename)
            
            # Send results in chunks
            if len(ml_results) > 4000:
                chunks = [ml_results[i:i+4000] for i in range(0, len(ml_results), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == 0 and callback:
                        await update.callback_query.edit_message_text(chunk, parse_mode='Markdown')
                    else:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=chunk,
                            parse_mode='Markdown'
                        )
            else:
                if callback:
                    await update.callback_query.edit_message_text(ml_results, parse_mode='Markdown')
                else:
                    await update.message.reply_text(ml_results, parse_mode='Markdown')
            
            # Generate ML visualizations
            await self.send_ml_charts(update, context, X, X_scaled, numeric_cols)
            
        except Exception as e:
            error_msg = f"❌ **ML Analysis Error:** {str(e)}"
            if callback:
                await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def generate_report(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Generate comprehensive analytical report"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "📋 **Generating comprehensive report...** Analyzing all aspects of your data."
            if callback:
                await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(progress_text, parse_mode='Markdown')
            
            # Generate full report
            report = self.generate_comprehensive_report(df, filename)
            
            # Send report in multiple messages
            sections = report.split('\n\n---\n\n')
            for i, section in enumerate(sections):
                if section.strip():
                    if i == 0 and callback:
                        await update.callback_query.edit_message_text(section, parse_mode='Markdown')
                    else:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=section,
                            parse_mode='Markdown'
                        )
            
            # Generate report visualizations
            await self.send_report_charts(update, context, df)
            
        except Exception as e:
            error_msg = f"❌ **Report Generation Error:** {str(e)}"
            if callback:
                await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    async def advanced_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE, callback=False):
        """Advanced statistical analysis"""
        if 'dataframe' not in context.user_data:
            message_text = "📁 **No data loaded!**\nPlease upload a CSV or Excel file first."
            if callback:
                await update.callback_query.edit_message_text(message_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(message_text, parse_mode='Markdown')
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            progress_text = "📉 **Computing advanced statistics...** Skewness, kurtosis, normality tests & more."
            if callback:
                await update.callback_query.edit_message_text(progress_text, parse_mode='Markdown')
            else:
                await update.message.reply_text(progress_text, parse_mode='Markdown')
            
            # Advanced statistical analysis
            stats_results = self.compute_advanced_statistics(df, filename)
            
            # Send results
            if len(stats_results) > 4000:
                chunks = [stats_results[i:i+4000] for i in range(0, len(stats_results), 4000)]
                for i, chunk in enumerate(chunks):
                    if i == 0 and callback:
                        await update.callback_query.edit_message_text(chunk, parse_mode='Markdown')
                    else:
                        await context.bot.send_message(
                            chat_id=update.effective_chat.id,
                            text=chunk,
                            parse_mode='Markdown'
                        )
            else:
                if callback:
                    await update.callback_query.edit_message_text(stats_results, parse_mode='Markdown')
                else:
                    await update.message.reply_text(stats_results, parse_mode='Markdown')
            
            # Generate statistical charts
            await self.send_statistical_charts(update, context, df)
            
        except Exception as e:
            error_msg = f"❌ **Statistical Analysis Error:** {str(e)}"
            if callback:
                await update.callback_query.edit_message_text(error_msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(error_msg, parse_mode='Markdown')
    
    # ================================================================
    #                      MESSAGE AND FILE HANDLERS
    # ================================================================
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages from users"""
        text = update.message.text.lower()
        
        if any(word in text for word in ['hello', 'hi', 'hey']):
            await update.message.reply_text("👋 Hello! Send /start to begin!")
        elif 'help' in text:
            await self.help_command(update, context)
        elif any(word in text for word in ['thanks', 'thank you']):
            await update.message.reply_text("😊 You're welcome! Happy to help!")
        elif any(word in text for word in ['chart', 'graph', 'plot']):
            await update.message.reply_text(
                "📈 To create charts:\n"
                "1. Upload a data file (CSV/Excel)\n"
                "2. Use /visualize or /charts command"
            )
        else:
            await update.message.reply_text(
                "🤔 I don't understand.\n"
                "Send /help for available commands or upload a data file."
            )
    
    # ================================================================
    #                      DATA ANALYSIS CORE METHODS
    # ================================================================
    
    def quick_analysis(self, df, filename):
        """
        Perform quick data analysis with quality metrics.
        
        Args:
            df: Pandas DataFrame with uploaded data
            filename: Name of the uploaded file
            
        Returns:
            str: Formatted analysis results with metrics and insights
        """
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        datetime_cols = df.select_dtypes(include=['datetime']).columns
        
        # Data quality metrics
        missing_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()
        total_cells = len(df) * len(df.columns)
        completeness = ((total_cells - missing_count) / total_cells * 100) if total_cells > 0 else 0
        
        # Data insights
        data_quality = "🟢 Excellent" if completeness > 95 else "🟡 Good" if completeness > 80 else "🔴 Needs Attention"
        dataset_size = "Large" if len(df) > 10000 else "Medium" if len(df) > 1000 else "Small"
        
        analysis = f"""
📊 **File Analysis: `{filename}`**

📈 **Dataset Overview:**
• **Size:** {len(df):,} rows × {len(df.columns)} columns ({dataset_size} dataset)
• **Memory:** {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
• **Quality:** {data_quality} ({completeness:.1f}% complete)

🔢 **Data Types Distribution:**
• **Numeric:** {len(numeric_cols)} columns
• **Text/Categorical:** {len(text_cols)} columns  
• **DateTime:** {len(datetime_cols)} columns

🔍 **Data Quality Assessment:**
• **Missing Values:** {missing_count:,} ({100 * missing_count / total_cells:.1f}%)
• **Duplicate Rows:** {duplicate_count:,} ({100 * duplicate_count / len(df):.1f}%)
• **Unique Rows:** {len(df) - duplicate_count:,}

📉 **Column Missing Data Summary:**"""
        
        # Add missing data details for columns
        missing_by_col = df.isnull().sum().sort_values(ascending=False)
        columns_with_missing = missing_by_col[missing_by_col > 0]
        
        if len(columns_with_missing) > 0:
            for col, missing_count in columns_with_missing.head(5).items():
                missing_pct = (missing_count / len(df)) * 100
                status = "🔴" if missing_pct > 20 else "🟡" if missing_pct > 5 else "🟢"
                analysis += f"\n• {status} **{col}**: {missing_pct:.1f}% missing ({missing_count:,} values)"
        else:
            analysis += "\n• ✅ **No missing data found** - Excellent data quality!"
        
        analysis += f"""

✅ **Status:** Data successfully loaded and validated!
📊 Use the menu button (□) or options below to continue analysis.
        """
        
        return analysis
    
    def enhanced_detailed_analysis(self, df, filename):
        """Enhanced detailed analysis with comprehensive insights"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        
        analysis = f"""
🔍 **Enhanced Analysis: `{filename}`**

📊 **Statistical Summary:**
        """
        
        # Enhanced statistics for numeric columns
        for col in numeric_cols[:5]:
            stats = df[col].describe()
            skewness = df[col].skew()
            kurtosis = df[col].kurtosis()
            
            # Data distribution assessment
            if abs(skewness) < 0.5:
                dist_desc = "Normal"
            elif abs(skewness) < 1:
                dist_desc = "Moderate Skew"
            else:
                dist_desc = "Highly Skewed"
                
            analysis += f"""
**{col}:**
• Mean: {stats['mean']:.3f} | Median: {stats['50%']:.3f}
• Range: {stats['min']:.2f} - {stats['max']:.2f}
• Std Dev: {stats['std']:.3f} | IQR: {stats['75%'] - stats['25%']:.2f}
• Distribution: {dist_desc} (Skew: {skewness:.2f})
• Missing: {df[col].isnull().sum()} ({100 * df[col].isnull().sum() / len(df):.1f}%)
"""

        # Correlation insights
        if len(numeric_cols) > 1:
            analysis += f"\n🔗 **Correlation Insights:**\n"
            corr_matrix = df[numeric_cols].corr()
            
            # Find significant correlations
            correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.3:  # Lower threshold for more insights
                        strength = "Strong" if abs(corr_val) > 0.7 else "Moderate" if abs(corr_val) > 0.5 else "Weak"
                        correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val, strength))
            
            if correlations:
                correlations.sort(key=lambda x: abs(x[2]), reverse=True)
                for col1, col2, corr_val, strength in correlations[:8]:
                    direction = "+" if corr_val > 0 else "-"
                    analysis += f"• **{col1}** ↔ **{col2}**: {corr_val:.3f} ({strength} {direction})\n"
            else:
                analysis += "• No significant correlations detected\n"

        # Missing data analysis for all columns
        missing_by_col = df.isnull().sum().sort_values(ascending=False)
        if missing_by_col.sum() > 0:
            analysis += f"\n📉 **Missing Data Analysis:**\n"
            top_missing = missing_by_col[missing_by_col > 0].head(5)
            for col, missing_count in top_missing.items():
                missing_pct = (missing_count / len(df)) * 100
                status = "⚠️" if missing_pct > 10 else "🟡"
                analysis += f"• {status} **{col}**: {missing_pct:.1f}% missing ({missing_count:,} values)\n"
        
        # Data quality insights
        analysis += f"\n🎯 **Data Quality & Business Insights:**\n"
        
        # Dataset characteristics
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
        duplicate_pct = df.duplicated().sum() / len(df) * 100
        
        if len(df) > 50000:
            analysis += "• 🚀 **Large Scale Dataset** - Excellent for ML models\n"
        elif len(df) > 10000:
            analysis += "• 📈 **Substantial Dataset** - Good for statistical analysis\n"
        elif len(df) > 1000:
            analysis += "• 📊 **Medium Dataset** - Suitable for basic analytics\n"
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
        
        if len(text_cols) > 0:
            analysis += f"• 📝 **Text Analysis Available** - {len(text_cols)} categorical columns\n"

        # Actionable recommendations
        analysis += f"\n💡 **Recommendations:**\n"
        
        if missing_pct > 10:
            analysis += "• Consider data imputation or row removal\n"
        if duplicate_pct > 2:
            analysis += "• Remove duplicate records for cleaner analysis\n"
        if len(numeric_cols) >= 3:
            analysis += "• Explore clustering and dimensionality reduction\n"
        if any(df[col].skew() > 2 for col in numeric_cols):
            analysis += "• Apply log transformation for skewed variables\n"
        
        return analysis
    
    # ================================================================
    #                      VISUALIZATION METHODS
    # ================================================================
    
    async def send_basic_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """
        Generate and send basic visualization charts.
        
        Creates a dashboard with distribution, correlation, and scatter plots
        using Plotly for interactive charts.
        """
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) == 0:
                await update.message.reply_text("📊 No numeric columns found for visualization")
                return
            
            # Create figure with subplots
            fig = make_subplots(
                rows=2, cols=2,
                subplot_titles=('Distribution', 'Box Plot', 'Correlation Matrix', 'Time Series'),
                specs=[[{'type': 'histogram'}, {'type': 'box'}],
                       [{'type': 'heatmap'}, {'type': 'scatter'}]]
            )
            
            # 1. Distribution plot for first numeric column
            col = numeric_cols[0]
            fig.add_trace(
                go.Histogram(x=df[col], name=col, showlegend=False),
                row=1, col=1
            )
            
            # 2. Box plot for first few numeric columns
            for i, col in enumerate(numeric_cols[:3]):
                fig.add_trace(
                    go.Box(y=df[col], name=col),
                    row=1, col=2
                )
            
            # 3. Correlation matrix if multiple numeric columns
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
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
            
            # 4. Scatter plot if at least 2 numeric columns
            if len(numeric_cols) >= 2:
                fig.add_trace(
                    go.Scatter(
                        x=df[numeric_cols[0]], 
                        y=df[numeric_cols[1]],
                        mode='markers',
                        name=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                        showlegend=False
                    ),
                    row=2, col=2
                )
            
            # Update layout
            fig.update_layout(
                title_text="Data Analysis Dashboard",
                height=800,
                showlegend=True
            )
            
            # Save and send chart
            chart_path = 'data_analysis.png'
            fig.write_image(chart_path)
            
            with open(chart_path, 'rb') as chart_file:
                await update.message.reply_photo(
                    photo=chart_file,
                    caption="📊 Data Visualization Dashboard"
                )
            
            # Clean up
            os.remove(chart_path)
            
        except Exception as e:
            # Fallback to matplotlib if plotly fails
            await self.send_matplotlib_charts(update, context, df)
    
    async def send_matplotlib_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Fallback to matplotlib for charts"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) == 0:
                return
            
            # Create figure
            fig, axes = plt.subplots(2, 2, figsize=(14, 12))
            fig.suptitle('Data Analysis Dashboard', fontsize=18, fontweight='bold')
            plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.1, hspace=0.3, wspace=0.3)
            
            # 1. Histogram
            df[numeric_cols[0]].hist(ax=axes[0, 0], bins=30, edgecolor='black')
            axes[0, 0].set_title(f'Distribution of {numeric_cols[0]}')
            axes[0, 0].set_xlabel(numeric_cols[0])
            axes[0, 0].set_ylabel('Frequency')
            
            # 2. Box plot
            if len(numeric_cols) >= 3:
                df[numeric_cols[:3]].boxplot(ax=axes[0, 1])
                axes[0, 1].set_title('Box Plot')
                axes[0, 1].set_ylabel('Values')
            
            # 3. Correlation heatmap
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                im = axes[1, 0].imshow(corr_matrix, cmap='coolwarm', aspect='auto', vmin=-1, vmax=1)
                axes[1, 0].set_title('Correlation Matrix', fontsize=12)
                axes[1, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_yticks(range(len(corr_matrix.columns)))
                
                # Truncate long column names for better readability
                short_cols = [col[:10] + '..' if len(col) > 10 else col for col in corr_matrix.columns]
                
                axes[1, 0].set_xticklabels(short_cols, rotation=45, ha='right', fontsize=8)
                axes[1, 0].set_yticklabels(short_cols, fontsize=8)
                plt.colorbar(im, ax=axes[1, 0])
                
                # Add correlation values as text
                for i in range(len(corr_matrix.columns)):
                    for j in range(len(corr_matrix.columns)):
                        text = axes[1, 0].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                             ha="center", va="center", color="black", fontsize=6)
            
            # 4. Scatter plot
            if len(numeric_cols) >= 2:
                axes[1, 1].scatter(df[numeric_cols[0]], df[numeric_cols[1]], alpha=0.5)
                # Truncate long titles and labels
                col1_short = numeric_cols[0][:15] + '..' if len(numeric_cols[0]) > 15 else numeric_cols[0]
                col2_short = numeric_cols[1][:15] + '..' if len(numeric_cols[1]) > 15 else numeric_cols[1]
                axes[1, 1].set_title(f'{col1_short} vs {col2_short}', fontsize=12)
                axes[1, 1].set_xlabel(col1_short, fontsize=10)
                axes[1, 1].set_ylabel(col2_short, fontsize=10)
            
            plt.tight_layout()
            
            # Save and send
            chart_path = 'analysis_charts.png'
            plt.savefig(chart_path, dpi=100, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await update.message.reply_photo(
                    photo=chart_file,
                    caption="📊 Data Analysis Charts"
                )
            
            os.remove(chart_path)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error creating charts: {str(e)}")
    
    async def send_advanced_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send advanced chart set"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Create multiple individual charts
            charts_created = 0
            
            # 1. Distribution plots for each numeric column
            for col in numeric_cols[:3]:
                fig, ax = plt.subplots(figsize=(8, 6))
                df[col].hist(bins=30, ax=ax, edgecolor='black', alpha=0.7)
                ax.set_title(f'Distribution of {col}', fontsize=14)
                ax.set_xlabel(col)
                ax.set_ylabel('Frequency')
                ax.grid(True, alpha=0.3)
                
                chart_path = f'dist_{col}.png'
                plt.savefig(chart_path, dpi=100, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await update.message.reply_photo(
                        photo=chart_file,
                        caption=f"📊 Distribution: {col}"
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            # 2. Pair plot if multiple columns
            if len(numeric_cols) >= 2:
                fig, ax = plt.subplots(figsize=(10, 8))
                
                # Create scatter matrix
                pd.plotting.scatter_matrix(
                    df[numeric_cols[:4]], 
                    ax=ax if len(numeric_cols) < 2 else None,
                    figsize=(10, 8),
                    diagonal='hist',
                    alpha=0.5
                )
                
                plt.suptitle('Pair Plot Analysis', fontsize=14)
                plt.tight_layout()
                
                chart_path = 'pairplot.png'
                plt.savefig(chart_path, dpi=100, bbox_inches='tight')
                plt.close()
                
                with open(chart_path, 'rb') as chart_file:
                    await update.message.reply_photo(
                        photo=chart_file,
                        caption="📊 Pair Plot Analysis"
                    )
                
                os.remove(chart_path)
                charts_created += 1
            
            await update.message.reply_text(f"✅ Generated {charts_created} charts successfully!")
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error creating advanced charts: {str(e)}")
    
    # ================================================================
    #                      MACHINE LEARNING METHODS
    # ================================================================
    
    def perform_ml_analysis(self, X, X_scaled, numeric_cols, filename):
        """
        Perform comprehensive machine learning analysis.
        
        Includes clustering, PCA, and anomaly detection with detailed insights.
        
        Args:
            X: Original feature matrix
            X_scaled: Standardized feature matrix
            numeric_cols: List of numeric column names
            filename: Name of analyzed file
            
        Returns:
            str: Formatted ML analysis results
        """
        results = f"""
🤖 **Machine Learning Analysis: `{filename}`**

🎯 **Clustering Analysis (K-Means):**
        """
        
        # Optimal number of clusters using silhouette score
        best_k = 2
        best_score = -1
        silhouette_scores = []
        
        for k in range(2, min(8, len(X)//2)):
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
        
        # Perform clustering with optimal k
        kmeans = KMeans(n_clusters=best_k, random_state=42, n_init=10)
        cluster_labels = kmeans.fit_predict(X_scaled)
        
        results += f"""
• **Optimal Clusters:** {best_k} (Silhouette Score: {best_score:.3f})
• **Cluster Distribution:**
"""
        
        unique, counts = np.unique(cluster_labels, return_counts=True)
        for cluster, count in zip(unique, counts):
            percentage = (count / len(cluster_labels)) * 100
            results += f"  - Cluster {cluster}: {count} points ({percentage:.1f}%)\n"
        
        # PCA Analysis
        results += f"""

📉 **Principal Component Analysis (PCA):**
"""
        
        pca = PCA()
        X_pca = pca.fit_transform(X_scaled)
        
        # Cumulative explained variance
        cumsum_var = np.cumsum(pca.explained_variance_ratio_)
        n_components_80 = np.argmax(cumsum_var >= 0.8) + 1
        n_components_95 = np.argmax(cumsum_var >= 0.95) + 1
        
        results += f"""
• **Components for 80% variance:** {n_components_80}/{len(numeric_cols)}
• **Components for 95% variance:** {n_components_95}/{len(numeric_cols)}
• **First 3 Components Variance:** {pca.explained_variance_ratio_[:3].sum():.1%}

**Top Feature Loadings (PC1):**
"""
        
        # Feature importance in first principal component
        pc1_loadings = abs(pca.components_[0])
        feature_importance = list(zip(numeric_cols, pc1_loadings))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        for feature, importance in feature_importance[:5]:
            results += f"• **{feature}**: {importance:.3f}\n"
        
        # Anomaly Detection
        results += f"""

🔍 **Anomaly Detection (Isolation Forest):**
"""
        
        iso_forest = IsolationForest(contamination=0.1, random_state=42)
        anomaly_labels = iso_forest.fit_predict(X_scaled)
        n_anomalies = np.sum(anomaly_labels == -1)
        anomaly_pct = (n_anomalies / len(X)) * 100
        
        results += f"""
• **Anomalies Detected:** {n_anomalies} ({anomaly_pct:.1f}%)
• **Normal Points:** {len(X) - n_anomalies} ({100 - anomaly_pct:.1f}%)
• **Contamination Level:** 10% threshold

💡 **ML Insights:**
"""
        
        # Business insights
        if best_score > 0.5:
            results += "• ✅ **Clear Clustering Structure** - Well-defined groups found\n"
        elif best_score > 0.3:
            results += "• 🟡 **Moderate Clustering** - Some group patterns detected\n"
        else:
            results += "• 🔴 **Weak Clustering** - Data may be uniformly distributed\n"
        
        if n_components_80 <= 3:
            results += "• 📉 **Low Dimensionality** - Data can be simplified effectively\n"
        else:
            results += "• 📈 **High Dimensionality** - Complex feature relationships\n"
        
        if anomaly_pct > 15:
            results += "• ⚠️ **High Anomaly Rate** - Consider data quality review\n"
        elif anomaly_pct < 5:
            results += "• ✅ **Low Anomaly Rate** - Good data consistency\n"
        
        return results
    
    def generate_comprehensive_report(self, df, filename):
        """Generate comprehensive analytical report with insights"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        
        # Executive Summary
        report = f"""
📋 **COMPREHENSIVE DATA ANALYSIS REPORT**

📊 **Executive Summary: `{filename}`**

**Dataset Profile:**
• Size: {len(df):,} records × {len(df.columns)} features
• Data Types: {len(numeric_cols)} numeric, {len(text_cols)} categorical
• Quality Score: {((df.count().sum() / (len(df) * len(df.columns))) * 100):.1f}%

---

🔍 **Data Quality Assessment:**
        """
        
        # Data quality metrics
        missing_total = df.isnull().sum().sum()
        missing_pct = (missing_total / (len(df) * len(df.columns))) * 100
        duplicates = df.duplicated().sum()
        
        quality_grade = "A" if missing_pct < 5 else "B" if missing_pct < 15 else "C"
        
        report += f"""
• **Overall Grade:** {quality_grade}
• **Missing Data:** {missing_total:,} values ({missing_pct:.2f}%)
• **Duplicate Records:** {duplicates:,} ({100 * duplicates / len(df):.1f}%)
• **Data Integrity:** {'High' if missing_pct < 10 else 'Moderate' if missing_pct < 25 else 'Low'}

**Column-wise Quality:**
"""
        
        # Show columns with most missing data first
        missing_by_col = df.isnull().sum().sort_values(ascending=False)
        top_missing_cols = missing_by_col.head(8)  # Top 8 columns with most missing data
        
        for col in top_missing_cols.index:
            missing_col = missing_by_col[col]
            missing_col_pct = (missing_col / len(df)) * 100
            status = "✅" if missing_col_pct < 5 else "⚠️" if missing_col_pct < 20 else "❌"
            report += f"• {status} **{col}**: {missing_col_pct:.1f}% missing ({missing_col:,} values)\n"

        # Statistical insights for numeric data
        if len(numeric_cols) > 0:
            report += f"""

---

📈 **Statistical Insights:**

**Key Metrics:**
"""
            
            for col in numeric_cols[:5]:
                stats = df[col].describe()
                cv = stats['std'] / stats['mean'] if stats['mean'] != 0 else 0
                variability = "High" if cv > 1 else "Moderate" if cv > 0.3 else "Low"
                
                report += f"""
**{col}:**
• Mean: {stats['mean']:.2f} ± {stats['std']:.2f}
• Range: [{stats['min']:.1f}, {stats['max']:.1f}]
• Variability: {variability} (CV: {cv:.2f})
"""

        # Business recommendations
        report += f"""

---

💡 **Strategic Recommendations:**

**Data Management:**
"""
        
        if missing_pct > 15:
            report += "• 🔴 **Critical**: Implement data quality controls and validation\n"
        elif missing_pct > 5:
            report += "• 🟡 **Important**: Consider data imputation strategies\n"
        else:
            report += "• ✅ **Excellent**: Data quality meets professional standards\n"
        
        if duplicates > len(df) * 0.02:  # More than 2% duplicates
            report += "• ⚠️ **Action Required**: Remove duplicate records\n"
        
        # Analytics recommendations
        report += f"""
**Analytics Opportunities:**
"""
        
        if len(numeric_cols) >= 5:
            report += "• 🤖 **Machine Learning**: Suitable for predictive modeling\n"
            report += "• 📊 **Advanced Analytics**: Clustering and segmentation analysis\n"
        
        if len(numeric_cols) >= 3:
            report += "• 📈 **Statistical Modeling**: Correlation and regression analysis\n"
        
        if len(text_cols) > 0:
            report += "• 📝 **Categorical Analysis**: Cross-tabulation and chi-square tests\n"
        
        # Performance metrics
        report += f"""

---

⚡ **Performance Metrics:**

• **Processing Time**: Optimized for {len(df):,} records
• **Memory Usage**: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB
• **Complexity Score**: {'High' if len(df.columns) > 20 else 'Medium' if len(df.columns) > 10 else 'Low'}

**Next Steps:**
1. Address data quality issues identified above
2. Explore relationships between key variables  
3. Consider advanced analytics based on recommendations
4. Monitor data quality over time

---

📊 **Report Generated**: {datetime.now().strftime('%Y-%m-%d')}
        """
        
        return report
    
    def compute_advanced_statistics(self, df, filename):
        """Compute advanced statistical metrics"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        results = f"""
📉 **Advanced Statistical Analysis: `{filename}`**

🔢 **Distribution Analysis:**
        """
        
        for col in numeric_cols[:5]:
            data = df[col].dropna()
            
            if len(data) < 3:
                continue
                
            # Advanced statistics
            skewness = data.skew()
            kurtosis = data.kurtosis()
            
            # Distribution classification
            if abs(skewness) < 0.5:
                skew_desc = "Approximately Normal"
            elif abs(skewness) < 1:
                skew_desc = "Moderately Skewed"
            else:
                skew_desc = "Highly Skewed"
            
            # Kurtosis interpretation
            if kurtosis > 3:
                kurt_desc = "Heavy-tailed (Leptokurtic)"
            elif kurtosis < -1:
                kurt_desc = "Light-tailed (Platykurtic)"
            else:
                kurt_desc = "Normal-tailed (Mesokurtic)"
            
            # Outlier detection using IQR
            Q1 = data.quantile(0.25)
            Q3 = data.quantile(0.75)
            IQR = Q3 - Q1
            outliers = data[(data < Q1 - 1.5 * IQR) | (data > Q3 + 1.5 * IQR)]
            outlier_pct = (len(outliers) / len(data)) * 100
            
            results += f"""
**{col}:**
• Skewness: {skewness:.3f} ({skew_desc})
• Kurtosis: {kurtosis:.3f} ({kurt_desc})
• Outliers: {len(outliers)} ({outlier_pct:.1f}%) using IQR method
• Coefficient of Variation: {(data.std() / data.mean()):.3f}
"""

        # Correlation matrix analysis
        if len(numeric_cols) > 1:
            results += f"""

🔗 **Correlation Matrix Analysis:**
"""
            
            corr_matrix = df[numeric_cols].corr()
            
            # Find strongest correlations
            correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if not np.isnan(corr_val):
                        correlations.append((
                            corr_matrix.columns[i], 
                            corr_matrix.columns[j], 
                            corr_val
                        ))
            
            # Sort by absolute correlation value
            correlations.sort(key=lambda x: abs(x[2]), reverse=True)
            
            results += "**Top Correlations:**\n"
            for col1, col2, corr_val in correlations[:8]:
                strength = "Very Strong" if abs(corr_val) > 0.8 else "Strong" if abs(corr_val) > 0.6 else "Moderate" if abs(corr_val) > 0.4 else "Weak"
                direction = "Positive" if corr_val > 0 else "Negative"
                results += f"• **{col1}** × **{col2}**: {corr_val:.3f} ({strength} {direction})\n"

        # Statistical tests and insights
        results += f"""

🧪 **Statistical Insights:**

**Data Distribution Summary:**
"""
        
        # Overall dataset characteristics
        total_variance = df[numeric_cols].var().sum() if len(numeric_cols) > 0 else 0
        
        if len(numeric_cols) > 0:
            avg_skewness = abs(df[numeric_cols].skew().mean())
            if avg_skewness < 0.5:
                results += "• ✅ **Distribution**: Generally normal across variables\n"
            elif avg_skewness < 1:
                results += "• 🟡 **Distribution**: Moderate skewness present\n"
            else:
                results += "• 🔴 **Distribution**: High skewness - consider transformations\n"
        
        # Multicollinearity check
        if len(numeric_cols) > 1:
            high_corr_pairs = sum(1 for _, _, corr in correlations if abs(corr) > 0.7)
            if high_corr_pairs > 0:
                results += f"• ⚠️ **Multicollinearity**: {high_corr_pairs} highly correlated pairs detected\n"
            else:
                results += "• ✅ **Independence**: Low multicollinearity between variables\n"
        
        # Data quality indicators
        results += f"""
**Quality Indicators:**
• **Completeness**: {((df.count().sum() / (len(df) * len(df.columns))) * 100):.1f}%
• **Consistency**: {'High' if df.duplicated().sum() < len(df) * 0.02 else 'Moderate'}
• **Variability**: {'High' if total_variance > 100 else 'Moderate' if total_variance > 10 else 'Low'}

💡 **Statistical Recommendations:**
"""
        
        if avg_skewness > 1:
            results += "• Consider log or Box-Cox transformations for skewed variables\n"
        if high_corr_pairs > 0:
            results += "• Apply dimensionality reduction techniques (PCA)\n"
        if any(df[col].std() / df[col].mean() > 2 for col in numeric_cols):
            results += "• Standardize variables before machine learning algorithms\n"
        
        return results
    
    async def send_enhanced_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send enhanced visualization suite"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            if len(numeric_cols) == 0:
                await context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="📊 No numeric columns found for visualization"
                )
                return

            # Enhanced dashboard with subplots
            fig = make_subplots(
                rows=3, cols=2,
                subplot_titles=(
                    'Distribution Analysis', 'Box Plot Comparison',
                    'Correlation Heatmap', 'Scatter Plot Matrix',  
                    'Statistical Summary', 'Trend Analysis'
                ),
                specs=[
                    [{'type': 'histogram'}, {'type': 'box'}],
                    [{'type': 'heatmap'}, {'type': 'scatter'}],
                    [{'type': 'bar'}, {'type': 'scatter'}]
                ]
            )
            
            # 1. Enhanced distribution plot
            col = numeric_cols[0]
            fig.add_trace(
                go.Histogram(
                    x=df[col], 
                    name=col,
                    nbinsx=30,
                    showlegend=False,
                    marker_color='lightblue',
                    opacity=0.8
                ),
                row=1, col=1
            )
            
            # 2. Multi-column box plot
            for i, col in enumerate(numeric_cols[:4]):
                fig.add_trace(
                    go.Box(
                        y=df[col], 
                        name=col,
                        boxpoints='outliers',
                        marker_color=px.colors.qualitative.Set1[i % len(px.colors.qualitative.Set1)]
                    ),
                    row=1, col=2
                )
            
            # 3. Enhanced correlation heatmap
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                fig.add_trace(
                    go.Heatmap(
                        z=corr_matrix.values,
                        x=corr_matrix.columns,
                        y=corr_matrix.columns,
                        colorscale='RdBu',
                        zmid=0,
                        showscale=True,
                        text=np.round(corr_matrix.values, 2),
                        texttemplate='%{text}',
                        textfont={"size": 10}
                    ),
                    row=2, col=1
                )
            
            # 4. Enhanced scatter plot
            if len(numeric_cols) >= 2:
                fig.add_trace(
                    go.Scatter(
                        x=df[numeric_cols[0]], 
                        y=df[numeric_cols[1]],
                        mode='markers',
                        name=f"{numeric_cols[0]} vs {numeric_cols[1]}",
                        marker=dict(
                            size=8,
                            opacity=0.6,
                            color=df[numeric_cols[0]] if len(numeric_cols) >= 3 else 'blue',
                            colorscale='viridis',
                            showscale=True
                        ),
                        showlegend=False
                    ),
                    row=2, col=2
                )
            
            # 5. Statistical summary bar chart
            stats_data = []
            for col in numeric_cols[:5]:
                stats_data.append(df[col].mean())
            
            fig.add_trace(
                go.Bar(
                    x=numeric_cols[:5],
                    y=stats_data,
                    name='Mean Values',
                    showlegend=False,
                    marker_color='lightgreen'
                ),
                row=3, col=1
            )
            
            # 6. Trend analysis (if applicable)
            if len(numeric_cols) >= 2:
                fig.add_trace(
                    go.Scatter(
                        x=list(range(len(df))),
                        y=df[numeric_cols[0]].rolling(window=min(20, len(df)//10)).mean(),
                        mode='lines',
                        name=f'{numeric_cols[0]} Trend',
                        showlegend=False,
                        line=dict(color='red', width=2)
                    ),
                    row=3, col=2
                )
            
            # Update layout
            fig.update_layout(
                title_text="📊 Enhanced Data Analysis Dashboard",
                height=1200,
                showlegend=True,
                title_x=0.5
            )
            
            # Save and send enhanced chart
            chart_path = 'enhanced_dashboard.png'
            fig.write_image(chart_path, width=1200, height=1200)
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="📊 **Enhanced Analytics Dashboard**\n\nComprehensive visualization suite with distribution, correlation, and trend analysis."
                )
            
            os.remove(chart_path)
            
        except Exception as e:
            await self.send_matplotlib_charts(update, context, df)
    
    async def send_ml_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, X, X_scaled, numeric_cols):
        """Send machine learning visualization charts"""
        try:
            # Create ML visualization dashboard
            fig, axes = plt.subplots(2, 2, figsize=(16, 14))
            fig.suptitle('🤖 Machine Learning Analysis Dashboard', fontsize=18, fontweight='bold')
            plt.subplots_adjust(left=0.1, right=0.95, top=0.93, bottom=0.1, hspace=0.3, wspace=0.3)
            
            # 1. Clustering visualization
            kmeans = KMeans(n_clusters=3, random_state=42)
            cluster_labels = kmeans.fit_predict(X_scaled)
            
            if len(numeric_cols) >= 2:
                scatter = axes[0, 0].scatter(X.iloc[:, 0], X.iloc[:, 1], c=cluster_labels, cmap='viridis', alpha=0.7)
                axes[0, 0].set_title('K-Means Clustering Results', fontsize=12)
                # Truncate long column names
                xlabel = numeric_cols[0][:20] + '...' if len(numeric_cols[0]) > 20 else numeric_cols[0]
                ylabel = numeric_cols[1][:20] + '...' if len(numeric_cols[1]) > 20 else numeric_cols[1]
                axes[0, 0].set_xlabel(xlabel, fontsize=10)
                axes[0, 0].set_ylabel(ylabel, fontsize=10)
                plt.colorbar(scatter, ax=axes[0, 0])
            
            # 2. PCA visualization
            pca = PCA()
            X_pca = pca.fit_transform(X_scaled)
            
            axes[0, 1].plot(range(1, len(pca.explained_variance_ratio_) + 1), 
                           np.cumsum(pca.explained_variance_ratio_), 'bo-')
            axes[0, 1].set_title('PCA: Cumulative Explained Variance')
            axes[0, 1].set_xlabel('Principal Components')
            axes[0, 1].set_ylabel('Cumulative Explained Variance')
            axes[0, 1].grid(True, alpha=0.3)
            
            # 3. Feature importance (using Random Forest)
            if len(X) > 10 and len(numeric_cols) > 1:
                # Use first column as target for feature importance demo
                rf = RandomForestRegressor(n_estimators=100, random_state=42)
                y_temp = X.iloc[:, 0]  # Use first column as pseudo-target
                X_temp = X.iloc[:, 1:]  # Rest as features
                
                if len(X_temp.columns) > 0:
                    rf.fit(X_temp, y_temp)
                    importances = rf.feature_importances_
                    
                    # Truncate long column names for better visibility
                    shortened_cols = [col[:15] + '...' if len(col) > 15 else col for col in X_temp.columns]
                    
                    axes[1, 0].barh(range(len(importances)), importances, color='lightgreen')
                    axes[1, 0].set_yticks(range(len(importances)))
                    axes[1, 0].set_yticklabels(shortened_cols, fontsize=8)
                    axes[1, 0].set_title('Feature Importance (Random Forest)', fontsize=12)
                    axes[1, 0].set_xlabel('Importance')
                    axes[1, 0].grid(True, alpha=0.3)
            
            # 4. Anomaly detection visualization  
            iso_forest = IsolationForest(contamination=0.1, random_state=42)
            anomaly_labels = iso_forest.fit_predict(X_scaled)
            
            if len(numeric_cols) >= 2:
                colors = ['red' if x == -1 else 'blue' for x in anomaly_labels]
                axes[1, 1].scatter(X.iloc[:, 0], X.iloc[:, 1], c=colors, alpha=0.6)
                axes[1, 1].set_title('Anomaly Detection (Red = Anomalies)', fontsize=12)
                # Truncate long column names
                xlabel = numeric_cols[0][:20] + '...' if len(numeric_cols[0]) > 20 else numeric_cols[0]
                ylabel = numeric_cols[1][:20] + '...' if len(numeric_cols[1]) > 20 else numeric_cols[1]
                axes[1, 1].set_xlabel(xlabel, fontsize=10)
                axes[1, 1].set_ylabel(ylabel, fontsize=10)
            
            plt.tight_layout()
            
            # Save and send ML charts
            chart_path = 'ml_analysis.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="🤖 **Machine Learning Analysis**\n\nClustering, PCA, Feature Importance & Anomaly Detection visualizations."
                )
            
            os.remove(chart_path)
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating ML charts: {str(e)}"
            )
    
    async def send_report_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send comprehensive report visualizations"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            
            # Create comprehensive report dashboard
            n_charts = min(4, len(numeric_cols))
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('📋 Comprehensive Analysis Report', fontsize=18, fontweight='bold')
            
            # Chart 1: Data quality overview
            missing_data = df.isnull().sum()
            top_missing = missing_data.nlargest(8)
            
            if len(top_missing) > 0 and top_missing.sum() > 0:
                axes[0, 0].barh(top_missing.index, top_missing.values, color='coral')
                axes[0, 0].set_title('Missing Data by Column')
                axes[0, 0].set_xlabel('Missing Count')
            else:
                axes[0, 0].text(0.5, 0.5, '✅ No Missing Data\nExcellent Quality!', 
                               ha='center', va='center', transform=axes[0, 0].transAxes,
                               fontsize=14, fontweight='bold')
                axes[0, 0].set_title('Data Quality Status')
            
            # Chart 2: Statistical distribution
            if len(numeric_cols) >= 1:
                col = numeric_cols[0]
                axes[0, 1].hist(df[col].dropna(), bins=30, alpha=0.7, color='lightblue', edgecolor='black')
                axes[0, 1].set_title(f'Distribution: {col}')
                axes[0, 1].set_xlabel(col)
                axes[0, 1].set_ylabel('Frequency')
                axes[0, 1].grid(True, alpha=0.3)
            
            # Chart 3: Correlation strength overview
            if len(numeric_cols) > 1:
                corr_matrix = df[numeric_cols].corr()
                im = axes[1, 0].imshow(corr_matrix, cmap='RdBu_r', aspect='auto', vmin=-1, vmax=1)
                axes[1, 0].set_title('Correlation Matrix Overview', fontsize=12)
                axes[1, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_yticks(range(len(corr_matrix.columns)))
                
                # Truncate long column names for better readability
                short_cols = [col[:8] + '..' if len(col) > 8 else col for col in corr_matrix.columns]
                
                axes[1, 0].set_xticklabels(short_cols, rotation=45, ha='right', fontsize=8)
                axes[1, 0].set_yticklabels(short_cols, fontsize=8)
                plt.colorbar(im, ax=axes[1, 0], fraction=0.046, pad=0.04)
                
                # Add correlation values as text for better readability
                for i in range(len(corr_matrix.columns)):
                    for j in range(len(corr_matrix.columns)):
                        text = axes[1, 0].text(j, i, f'{corr_matrix.iloc[i, j]:.2f}',
                                             ha="center", va="center", color="white" if abs(corr_matrix.iloc[i, j]) > 0.5 else "black", 
                                             fontsize=6, weight='bold')
            
            # Chart 4: Summary statistics
            if len(numeric_cols) >= 1:
                stats_data = df[numeric_cols[:5]].describe().loc[['mean', 'std', 'min', 'max']]
                
                x_pos = np.arange(len(stats_data.columns))
                width = 0.2
                
                for i, stat in enumerate(['mean', 'std', 'min', 'max']):
                    if stat in stats_data.index:
                        axes[1, 1].bar(x_pos + i * width, stats_data.loc[stat], 
                                     width, label=stat.capitalize(), alpha=0.8)
                
                axes[1, 1].set_title('Statistical Summary')
                axes[1, 1].set_xlabel('Variables')
                axes[1, 1].set_ylabel('Values')
                axes[1, 1].set_xticks(x_pos + width * 1.5)
                axes[1, 1].set_xticklabels(stats_data.columns, rotation=45, ha='right')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Save and send report charts
            chart_path = 'comprehensive_report.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="📋 **Comprehensive Report Dashboard**\n\nData quality, distributions, correlations & statistical summaries."
                )
            
            os.remove(chart_path)
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating report charts: {str(e)}"
            )
    
    async def send_statistical_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send advanced statistical visualization charts"""
        try:
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()[:4]
            
            if len(numeric_cols) == 0:
                return
            
            # Create statistical analysis dashboard
            fig, axes = plt.subplots(2, 2, figsize=(15, 12))
            fig.suptitle('📉 Advanced Statistical Analysis', fontsize=16, fontweight='bold')
            
            # Chart 1: Q-Q plots for normality assessment
            if len(numeric_cols) >= 1:
                from scipy.stats import probplot
                probplot(df[numeric_cols[0]].dropna(), dist="norm", plot=axes[0, 0])
                axes[0, 0].set_title(f'Q-Q Plot: {numeric_cols[0]}')
                axes[0, 0].grid(True, alpha=0.3)
            
            # Chart 2: Box plots with outlier analysis
            if len(numeric_cols) >= 1:
                df[numeric_cols[:min(4, len(numeric_cols))]].boxplot(ax=axes[0, 1])
                axes[0, 1].set_title('Box Plot Analysis (Outlier Detection)')
                axes[0, 1].tick_params(axis='x', rotation=45)
                axes[0, 1].grid(True, alpha=0.3)
            
            # Chart 3: Distribution comparison
            if len(numeric_cols) >= 2:
                for i, col in enumerate(numeric_cols[:2]):
                    axes[1, 0].hist(df[col].dropna(), bins=20, alpha=0.6, 
                                   label=col, density=True)
                axes[1, 0].set_title('Distribution Comparison')
                axes[1, 0].set_xlabel('Values')
                axes[1, 0].set_ylabel('Density')
                axes[1, 0].legend()
                axes[1, 0].grid(True, alpha=0.3)
            
            # Chart 4: Skewness and Kurtosis visualization  
            if len(numeric_cols) >= 1:
                skew_data = [df[col].skew() for col in numeric_cols]
                kurt_data = [df[col].kurtosis() for col in numeric_cols]
                
                x_pos = np.arange(len(numeric_cols))
                width = 0.35
                
                axes[1, 1].bar(x_pos - width/2, skew_data, width, label='Skewness', alpha=0.8)
                axes[1, 1].bar(x_pos + width/2, kurt_data, width, label='Kurtosis', alpha=0.8)
                axes[1, 1].set_title('Distribution Shape Analysis')
                axes[1, 1].set_xlabel('Variables')
                axes[1, 1].set_ylabel('Values')
                axes[1, 1].set_xticks(x_pos)
                axes[1, 1].set_xticklabels(numeric_cols, rotation=45, ha='right')
                axes[1, 1].legend()
                axes[1, 1].grid(True, alpha=0.3)
                axes[1, 1].axhline(y=0, color='black', linestyle='-', alpha=0.3)
            
            plt.tight_layout()
            
            # Save and send statistical charts
            chart_path = 'statistical_analysis.png'
            plt.savefig(chart_path, dpi=150, bbox_inches='tight')
            plt.close()
            
            with open(chart_path, 'rb') as chart_file:
                await context.bot.send_photo(
                    chat_id=update.effective_chat.id,
                    photo=chart_file,
                    caption="📉 **Advanced Statistical Analysis**\n\nNormality tests, outlier detection, distribution analysis & shape metrics."
                )
            
            os.remove(chart_path)
            
        except Exception as e:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"❌ Error creating statistical charts: {str(e)}"
            )
    
    # ================================================================
    #                      BOT RUNTIME METHODS
    # ================================================================
    
    def run(self):
        """
        Start the bot and begin polling for messages.
        
        This method initializes the bot and starts the main event loop
        to handle incoming messages from Telegram.
        """
        print("🤖 Starting DataBot Analytics Pro...")
        print(f"🔑 Token found: {TOKEN[:10]}...")
        print("✅ Bot is ready and operational!")
        print("📱 Find your bot on Telegram and send /start")
        print("🔄 Press Ctrl+C to stop the bot")
        print("👤 Created by: Artur")
        print("💝 Remember: Data is Love - take care of your data")
        self.application.run_polling()

# ========================================================================
#                           MAIN EXECUTION
# ========================================================================

if __name__ == "__main__":
    """
    Main execution block.
    
    Initializes and runs the DataBot Analytics Pro with proper error handling.
    Author: Artur
    Philosophy: "Data is Love - take care of your data"
    """
    try:
        bot = DataAnalyticsBot()
        bot.run()
    except ValueError as e:
        print(f"❌ Configuration Error: {e}")
        print("💡 Please check your .env file and bot token!")
        print("📝 Your .env file should contain:")
        print("TELEGRAM_TOKEN=your_telegram_bot_token_here")
        print("\n👤 Author: Artur")
        print("💝 Data is Love - take care of your data")
    except Exception as e:
        print(f"❌ Unexpected error occurred: {e}")
        print("💡 Please check your internet connection and bot configuration!")
        print("\n👤 Author: Artur") 
        print("💝 Data is Love - take care of your data")

import logging
from telegram import Update, InputFile
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
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

# Load environment variables
load_dotenv()

# Get token
TOKEN = os.getenv('TELEGRAM_TOKEN')

# Setup logging
logging.basicConfig(level=logging.INFO)

class DataAnalyticsBot:
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
        self.application.add_handler(MessageHandler(filters.Document.ALL, self.handle_document))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_text))
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start command"""
        welcome_text = """
🚀 Welcome to DataBot Analytics Pro!

I can analyze your data and create beautiful visualizations.

📋 Available commands:
/help - Show help
/analyze - Analyze loaded data
/visualize - Create quick visualization
/charts - Generate multiple charts

📁 Supported formats:
- CSV files
- Excel files (XLS, XLSX)

Send me a data file to start!
        """
        await update.message.reply_text(welcome_text)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command"""
        help_text = """
📊 DataBot Analytics - Commands:

🤖 Main commands:
/start - Start the bot
/help - Show this help
/analyze - Detailed data analysis
/visualize - Quick visualization
/charts - Generate chart set

📁 File handling:
- Send CSV, XLS, or XLSX file
- Files up to 20MB supported
- Automatic statistics and charts

📈 Visualizations:
- Line charts
- Bar charts
- Scatter plots
- Heatmaps
- Distribution plots
- Correlation matrices

💡 Usage example:
1. Send /start
2. Upload your data file
3. Get instant analysis & charts!
        """
        await update.message.reply_text(help_text)
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle document uploads"""
        try:
            file_name = update.message.document.file_name
            file_ext = os.path.splitext(file_name.lower())[1]
            
            # Check if file format is supported
            if file_ext not in ['.csv', '.xls', '.xlsx']:
                await update.message.reply_text(
                    "❌ Unsupported file format!\n"
                    "📁 Please send CSV, XLS, or XLSX files"
                )
                return
            
            await update.message.reply_text("📊 Processing your file...")
            
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
            await update.message.reply_text(analysis_text, parse_mode='Markdown')
            
            # Auto-generate basic visualization
            await self.send_basic_charts(update, context, df)
            
        except Exception as e:
            await update.message.reply_text(f"❌ Error processing file: {str(e)}")
    
    async def analyze(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Detailed data analysis"""
        if 'dataframe' not in context.user_data:
            await update.message.reply_text("📁 Please upload a data file first!")
            return
        
        df = context.user_data['dataframe']
        filename = context.user_data.get('filename', 'unknown')
        
        try:
            await update.message.reply_text("🔍 Performing detailed analysis...")
            
            # Detailed statistics
            detailed_analysis = self.detailed_analysis(df, filename)
            await update.message.reply_text(detailed_analysis, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(f"❌ Analysis error: {str(e)}")
    
    async def visualize(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Create quick visualization"""
        if 'dataframe' not in context.user_data:
            await update.message.reply_text("📁 Please upload a data file first!")
            return
        
        df = context.user_data['dataframe']
        await update.message.reply_text("📈 Creating visualizations...")
        await self.send_basic_charts(update, context, df)
    
    async def create_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Generate multiple chart types"""
        if 'dataframe' not in context.user_data:
            await update.message.reply_text("📁 Please upload a data file first!")
            return
        
        df = context.user_data['dataframe']
        await update.message.reply_text("🎨 Generating comprehensive charts...")
        await self.send_advanced_charts(update, context, df)
    
    async def handle_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
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
    
    def quick_analysis(self, df, filename):
        """Quick data analysis"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        text_cols = df.select_dtypes(include=['object']).columns
        datetime_cols = df.select_dtypes(include=['datetime']).columns
        
        # Data quality
        missing_count = df.isnull().sum().sum()
        duplicate_count = df.duplicated().sum()
        total_cells = len(df) * len(df.columns)
        completeness = ((total_cells - missing_count) / total_cells * 100) if total_cells > 0 else 0
        
        # Basic statistics
        analysis = f"""
📊 *File Analysis: {filename}*

📈 *Dataset Overview:*
- Rows: {len(df):,}
- Columns: {len(df.columns)}
- Memory usage: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB

🔢 *Data Types:*
- Numeric columns: {len(numeric_cols)}
- Text columns: {len(text_cols)}
- DateTime columns: {len(datetime_cols)}

📋 *Data Quality:*
- Missing values: {missing_count:,} ({100 * missing_count / total_cells:.1f}%)
- Duplicate rows: {duplicate_count:,}
- Data completeness: {completeness:.1f}%

✅ File successfully loaded! Use /analyze for detailed analysis or /visualize for charts.
        """
        
        return analysis
    
    def detailed_analysis(self, df, filename):
        """Detailed data analysis"""
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        analysis = f"""
🔍 *Detailed Analysis: {filename}*

📊 *Numeric Columns Statistics:*
        """
        
        # Statistics for first 5 numeric columns
        for col in numeric_cols[:5]:
            stats = df[col].describe()
            analysis += f"""
*{col}:*
- Mean: {stats['mean']:.2f}
- Median: {stats['50%']:.2f}
- Std Dev: {stats['std']:.2f}
- Min: {stats['min']:.2f}
- Max: {stats['max']:.2f}
- Q1: {stats['25%']:.2f}
- Q3: {stats['75%']:.2f}
"""
        
        # Correlations
        if len(numeric_cols) > 1:
            analysis += f"\n🔗 *Correlation Analysis:*\n"
            corr_matrix = df[numeric_cols].corr()
            
            # Find high correlations
            correlations = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    corr_val = corr_matrix.iloc[i, j]
                    if abs(corr_val) > 0.5:
                        correlations.append((corr_matrix.columns[i], corr_matrix.columns[j], corr_val))
            
            if correlations:
                correlations.sort(key=lambda x: abs(x[2]), reverse=True)
                for col1, col2, corr_val in correlations[:5]:
                    analysis += f"• {col1} ↔ {col2}: {corr_val:.3f}\n"
            else:
                analysis += "• No strong correlations found\n"
        
        # Insights
        analysis += f"\n💡 *Key Insights:*\n"
        
        if len(df) > 10000:
            analysis += "• Large dataset - suitable for machine learning\n"
        
        if len(numeric_cols) >= 3:
            analysis += "• Multiple numeric features available for analysis\n"
        
        missing_pct = df.isnull().sum().sum() / (len(df) * len(df.columns)) * 100
        if missing_pct > 10:
            analysis += f"• Consider data cleaning (missing: {missing_pct:.1f}%)\n"
        
        if duplicate_count := df.duplicated().sum():
            analysis += f"• Found {duplicate_count} duplicate rows\n"
        
        return analysis
    
    async def send_basic_charts(self, update: Update, context: ContextTypes.DEFAULT_TYPE, df):
        """Send basic charts to user"""
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
            fig, axes = plt.subplots(2, 2, figsize=(12, 10))
            fig.suptitle('Data Analysis Dashboard', fontsize=16)
            
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
                im = axes[1, 0].imshow(corr_matrix, cmap='coolwarm', aspect='auto')
                axes[1, 0].set_title('Correlation Matrix')
                axes[1, 0].set_xticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_yticks(range(len(corr_matrix.columns)))
                axes[1, 0].set_xticklabels(corr_matrix.columns, rotation=45, ha='right')
                axes[1, 0].set_yticklabels(corr_matrix.columns)
                plt.colorbar(im, ax=axes[1, 0])
            
            # 4. Scatter plot
            if len(numeric_cols) >= 2:
                axes[1, 1].scatter(df[numeric_cols[0]], df[numeric_cols[1]], alpha=0.5)
                axes[1, 1].set_title(f'{numeric_cols[0]} vs {numeric_cols[1]}')
                axes[1, 1].set_xlabel(numeric_cols[0])
                axes[1, 1].set_ylabel(numeric_cols[1])
            
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
    
    def run(self):
        """Run the bot"""
        print("🤖 Starting DataBot Analytics...")
        print(f"🔑 Token found: {TOKEN[:10]}...")
        print("✅ Bot is ready!")
        print("📱 Find your bot on Telegram and send /start")
        print("🔄 Press Ctrl+C to stop")
        self.application.run_polling()

if __name__ == "__main__":
    try:
        bot = DataAnalyticsBot()
        bot.run()
    except ValueError as e:
        print(f"❌ Error: {e}")
        print("💡 Check your .env file and bot token!")
        print("📝 Your .env file should contain:")
        print("TELEGRAM_TOKEN=your_token_here")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print("💡 Check your internet connection and bot token!")
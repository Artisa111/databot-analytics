# DataBot Analytics 📊🤖

[![CI](https://github.com/Artisa111/databot-analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/Artisa111/databot-analytics/actions/workflows/ci.yml)

A comprehensive data analytics platform combining a **Streamlit web application** and a **Telegram bot** for seamless data analysis, visualization, and insights generation.

## 🌟 Features

### Web Application (Streamlit)
- **📁 Data Upload**: Support for CSV, Excel, JSON files with automatic data cleaning
- **📈 Interactive Charts**: Advanced visualizations including 3D plots and correlation matrices
- **📊 Statistical Analysis**: Descriptive statistics, hypothesis testing, and data quality metrics
- **🤖 Machine Learning**: Clustering, PCA, anomaly detection with intuitive interfaces
- **🧪 A/B Testing**: Complete A/B test analysis with statistical significance testing
- **💾 Database Integration**: SQLite and PostgreSQL support for data storage and retrieval
- **📄 Report Generation**: Automated PDF reports and custom analytics summaries

### Telegram Bot
- **📁 File Analysis**: Upload files directly to Telegram for instant analysis
- **📊 Quick Stats**: Get immediate statistical summaries and insights
- **📈 Visualizations**: Generate charts and send them directly in chat
- **🔍 Data Exploration**: Interactive commands for exploring your datasets

## 🏗️ Architecture

```
DataBot Analytics
├── Web Service (Streamlit) - Always available on Railway
│   ├── Main dashboard and analytics interface
│   ├── File upload and data processing
│   └── Advanced visualizations and ML tools
├── Telegram Bot (Optional) - Runs if TELEGRAM_TOKEN is provided
│   ├── Chat-based data analysis
│   ├── File upload via Telegram
│   └── Quick insights and visualizations
└── Shared Components
    ├── Data processing utilities
    ├── Visualization engines
    └── Analytics functions
```

## 🚀 Quick Start

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Artisa111/databot-analytics.git
   cd databot-analytics
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables** (create `.env` file):
   ```env
   # Optional: Telegram Bot Token (if you want bot functionality)
   TELEGRAM_TOKEN=your_telegram_bot_token_here
   
   # Optional: Database connections
   DATABASE_URL=your_database_url_here
   ```

4. **Run the application**:
   ```bash
   python main.py
   ```

   This will start:
   - Streamlit web app on `http://localhost:8501`
   - Telegram bot (if `TELEGRAM_TOKEN` is provided)

### Railway Deployment

1. **Connect your GitHub repository** to Railway
2. **Set environment variables** in Railway dashboard:
   - `TELEGRAM_TOKEN` (optional): Your Telegram bot token
   - `PORT` (auto-set by Railway): Port for the web service
3. **Deploy**: Railway will automatically use `railway.toml` configuration

The application is designed to be **crash-resistant** - the web service will always run, even if the Telegram bot fails to start.

## 🔧 Environment Variables

| Variable | Required | Description | Default |
|----------|----------|-------------|---------|
| `PORT` | No | Port for Streamlit web service | `8501` |
| `TELEGRAM_TOKEN` | No | Telegram bot token for bot functionality | None |
| `DATABASE_URL` | No | PostgreSQL connection string | None |

## 📱 Telegram Bot Setup

1. **Create a bot** via [@BotFather](https://t.me/botfather) on Telegram
2. **Get your token** and add it to `.env` file or Railway environment variables
3. **Start a chat** with your bot and send `/start`

### Bot Commands
- `/start` - Welcome message and instructions
- `/help` - List all available commands
- `/analyze` - Detailed statistical analysis of uploaded data
- `/visualize` - Quick visualization generation
- `/charts` - Create multiple chart types

## 🛠️ Development

### Project Structure
```
├── main.py              # Main entry point (Railway-compatible)
├── app.py              # Streamlit web application
├── bot.py              # Telegram bot implementation
├── config.py           # Configuration and settings
├── requirements.txt    # Python dependencies
├── railway.toml        # Railway deployment configuration
├── .streamlit/         # Streamlit-specific configuration
│   └── config.toml
└── .github/            # GitHub Actions workflows
    └── workflows/
        └── ci.yml
```

### Running Tests
```bash
# Install test dependencies
pip install pytest

# Run tests (if available)
pytest -v
```

### Code Style
The project follows Python best practices:
- PEP 8 style guidelines
- Comprehensive error handling
- Modular design with separation of concerns
- Environment-based configuration

## 🚨 Troubleshooting

### Railway Deployment Issues

**Problem**: Service shows CRASHED status
- **Solution**: Check Railway logs. The web service should start even without `TELEGRAM_TOKEN`
- **Verify**: Environment variables are properly set in Railway dashboard

**Problem**: Bot not responding on Telegram
- **Check**: `TELEGRAM_TOKEN` is correctly set in environment variables
- **Verify**: Token has no trailing spaces or newlines
- **Test**: Bot functionality locally first

### Local Development Issues

**Problem**: Import errors or missing dependencies
- **Solution**: Reinstall requirements: `pip install -r requirements.txt`
- **Check**: Python version compatibility (3.8+)

**Problem**: Streamlit not starting
- **Solution**: Check if port 8501 is available
- **Alternative**: Use `streamlit run app.py --server.port 8502`

### Performance Issues

**Problem**: Large file uploads failing
- **Solution**: Use desktop browser instead of mobile
- **Alternative**: Use Telegram bot for file uploads
- **Check**: File size limits (Railway has specific limits)

## 🔄 CI/CD

The project includes GitHub Actions for:
- **Dependency Installation**: Automated pip install
- **Code Linting**: Basic Python syntax and style checks
- **Import Testing**: Verify all modules import correctly
- **Configuration Validation**: Check required config files exist

## 📊 Analytics Capabilities

### Statistical Analysis
- Descriptive statistics and data profiling
- Correlation analysis and feature relationships
- Outlier detection and data quality assessment
- A/B testing with statistical significance

### Machine Learning
- K-means clustering with automatic optimal cluster detection
- Principal Component Analysis (PCA) for dimensionality reduction
- Anomaly detection using multiple algorithms
- Feature importance and data insights

### Visualizations
- Interactive Plotly charts (scatter, line, bar, heatmaps)
- 3D visualizations and surface plots
- Geographic mapping with Folium
- Statistical distribution plots

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/Artisa111/databot-analytics/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Artisa111/databot-analytics/discussions)
- **Documentation**: This README and inline code comments

---

**Made with ❤️ for data analysts and scientists**

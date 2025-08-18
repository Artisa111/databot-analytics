# DataBot Analytics Pro 🚀

A powerful data analysis platform combining a **Telegram bot** and **web interface** for seamless data exploration, visualization, and analytics.

![Python](https://img.shields.io/badge/python-v3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## 🌟 Features

### Telegram Bot
- 📁 **File Upload**: Upload CSV, Excel files directly to Telegram
- 📊 **Instant Analysis**: Get statistical summaries and insights
- 📈 **Visualizations**: Generate charts and plots on-the-go
- 🤖 **Interactive Commands**: Use simple commands like `/analyze`, `/visualize`
- 📱 **Mobile Friendly**: Perfect for mobile data analysis

### Web Interface
- 🌐 **Streamlit App**: Beautiful, interactive web dashboard
- 📊 **Advanced Charts**: 3D plots, correlation matrices, interactive visualizations
- 🧪 **A/B Testing**: Built-in statistical testing tools
- 💾 **Database Integration**: SQLite and PostgreSQL support
- 📈 **Machine Learning**: Clustering, regression, classification
- 🌍 **Geographic Analysis**: Map visualizations with Folium

## 🏗️ Architecture

```
DataBot Analytics
├── 🤖 Telegram Bot (bot.py)     # Mobile-first data analysis
├── 🌐 Web Interface (app.py)    # Desktop-rich analytics  
├── 🚀 Launcher (main.py)        # Resilient deployment system
├── ⚙️ Configuration (config.py)  # Environment management
└── 📊 Utilities (utils.py)      # Shared analytics functions
```

### Resilient Deployment Design
- **Primary Process**: Streamlit web interface (monitored by Railway)
- **Secondary Process**: Telegram bot (isolated, can fail safely)
- **Zero Downtime**: Web stays alive even if bot encounters issues
- **Health Monitoring**: Railway healthcheck on web interface

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Artisa111/databot-analytics.git
cd databot-analytics
```

### 2. Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your values
nano .env
```

### 3. Configure Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Copy your bot token to `.env`:
```env
TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
```

### 4. Run Locally
```bash
# Start both web and bot
python main.py

# Or run individually:
python bot.py          # Bot only
streamlit run app.py   # Web only
```

Visit `http://localhost:8501` for the web interface.

## 🌐 Railway Deployment

### Automatic Deployment
1. **Fork** this repository
2. Connect your GitHub repo to [Railway](https://railway.app)
3. Add environment variable:
   - `TELEGRAM_TOKEN`: Your bot token
4. Deploy! 🚀

### Manual Railway Configuration
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway create
railway add --database postgresql  # Optional
railway deploy
```

The deployment is configured via `railway.toml`:
- **Start Command**: `python main.py`
- **Health Check**: Web interface on port from `$PORT`
- **Restart Policy**: Automatic restart on failure

## 📋 Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `TELEGRAM_TOKEN` | Bot token from @BotFather | Yes | `1234567890:ABC...` |
| `PORT` | Web server port (Railway sets this) | No | `8501` |
| `DATABASE_URL` | PostgreSQL connection string | No | `postgresql://...` |

## 🔧 Configuration

### Streamlit Configuration
The app uses `.streamlit/config.toml` for headless deployment:
```toml
[server]
headless = true
address = "0.0.0.0"
port = 8501
```

### Bot Configuration  
Bot settings are in `config.py`:
```python
# Customize colors, page settings, etc.
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e', 
    # ...
}
```

## 🔒 Security Best Practices

### Token Management
- ✅ **Never commit tokens**: Use environment variables only
- ✅ **Use .env files**: Keep secrets out of code  
- ✅ **Sanitize inputs**: Tokens are stripped of whitespace
- ✅ **Validate format**: Basic token format validation

### If Your Token Was Compromised
1. **Revoke old token**: Message @BotFather → `/revoke`
2. **Generate new token**: `/newbot` or `/token`
3. **Update environment**: Change `TELEGRAM_TOKEN` in deployment
4. **Optional cleanup**: Remove token from git history:
   ```bash
   # Use BFG or git-filter-branch (advanced)
   java -jar bfg.jar --replace-text passwords.txt .git
   ```

## 🛠️ Development

### Project Structure
```
databot-analytics/
├── .env.example          # Environment template
├── .gitignore           # Ignore secrets and temp files
├── requirements.txt     # Python dependencies
├── railway.toml        # Railway deployment config
├── main.py            # Resilient launcher
├── bot.py            # Telegram bot logic
├── app.py           # Streamlit web app
├── config.py        # Configuration management
├── utils.py         # Shared utilities
├── .streamlit/
│   └── config.toml  # Streamlit configuration
└── .github/
    └── workflows/
        └── ci.yml   # GitHub Actions CI/CD
```

### Running Tests
```bash
# Install development dependencies
pip install -r requirements.txt

# Run validation tests
python -c "from bot import DataAnalyticsBot; print('✅ Bot imports OK')"
python -c "import main; print('✅ Main launcher OK')"

# Check security
grep -r "token.*=" . --include="*.py" | grep -v "getenv"  # Should be empty
```

### Contributing
1. Fork the repository
2. Create feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push branch: `git push origin feature/amazing-feature`
5. Open Pull Request

## 📊 Usage Examples

### Telegram Bot Commands
```
/start - Get welcome message and instructions
/help - Show all available commands  
/analyze - Perform detailed statistical analysis
/visualize - Generate basic charts
/charts - Create advanced visualizations
```

### Web Interface Features
- **Upload Data**: Drag & drop CSV/Excel files
- **Statistical Analysis**: Descriptive stats, correlations
- **Visualizations**: Histograms, scatter plots, heatmaps
- **A/B Testing**: Statistical significance testing
- **Machine Learning**: Clustering, regression analysis
- **Database Tools**: SQL queries, data management

## 🐛 Troubleshooting

### Common Issues

**Bot not responding:**
```bash
# Check token format
echo $TELEGRAM_TOKEN | wc -c  # Should be ~45 characters

# Test bot locally
python bot.py
```

**Web interface not loading:**
```bash
# Check port binding
streamlit run app.py --server.port 8501

# Check logs
python main.py  # Look for error messages
```

**Railway deployment failing:**
- ✅ Check `TELEGRAM_TOKEN` environment variable is set
- ✅ Verify `railway.toml` configuration
- ✅ Check Railway build logs for errors
- ✅ Ensure dependencies in `requirements.txt` are correct

**Import errors:**
```bash
# Install missing dependencies
pip install -r requirements.txt

# Check Python version (3.9+ required)
python --version
```

### Getting Help
1. **Check logs**: Look at Railway logs or local console output
2. **Test locally**: Run `python main.py` to test locally first  
3. **Verify token**: Make sure `TELEGRAM_TOKEN` is correctly set
4. **Update dependencies**: `pip install -r requirements.txt --upgrade`

## 📈 Performance Tips

### For Large Datasets
- Use chunked processing for files > 100MB
- Enable database mode for persistent storage
- Consider data sampling for quick analysis

### Memory Optimization  
- Clear session state in Streamlit after analysis
- Use generators for large file processing
- Monitor memory usage with `htop` or similar

## 🤝 Support

- 📧 **Issues**: [GitHub Issues](https://github.com/Artisa111/databot-analytics/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/Artisa111/databot-analytics/discussions) 
- 🐛 **Bug Reports**: Use issue templates

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - Web app framework
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) - Telegram bot library
- [Plotly](https://plotly.com/) - Interactive visualizations
- [Railway](https://railway.app/) - Deployment platform

---

**Made with ❤️ for data enthusiasts everywhere!**

*Last updated: August 2025*

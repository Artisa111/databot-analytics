# 🚀 DataBot Analytics

A powerful Telegram bot and Streamlit web application for data analytics, visualization, and machine learning analysis.

## ✨ Features

- **📊 Telegram Bot**: Upload CSV/Excel files and get instant analysis via Telegram
- **🌐 Web Interface**: Comprehensive Streamlit dashboard for data exploration
- **📈 Advanced Analytics**: Statistical analysis, ML clustering, A/B testing
- **🎨 Rich Visualizations**: Interactive charts with Plotly and Seaborn
- **☁️ Railway Ready**: Optimized for cloud deployment with health checks

## 🤖 Telegram Bot Commands

- `/start` - Get welcome message and instructions
- `/help` - Show available commands
- `/analyze` - Detailed data analysis
- `/visualize` - Quick data visualization
- `/charts` - Generate multiple chart types

Simply send CSV or Excel files to get instant analytics!

## 🚀 Quick Start

### Local Development

1. **Clone and setup**:
```bash
git clone https://github.com/Artisa111/databot-analytics.git
cd databot-analytics
pip install -r requirements.txt
```

2. **Configure environment**:
```bash
cp .env.example .env
# Edit .env and add your TELEGRAM_TOKEN
```

3. **Get Telegram Bot Token**:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create new bot with `/newbot`
   - Copy the token (format: `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`)
   - Add to `.env` file

4. **Run locally**:
```bash
# Just the bot
python bot.py

# Or with web interface
streamlit run app.py
```

### 🚄 Railway Deployment

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new)

1. **Fork this repository**
2. **Deploy to Railway**:
   - Connect your GitHub account
   - Select this repository
   - Railway will auto-detect and deploy

3. **Set Environment Variables** in Railway dashboard:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   ```
   
   ⚠️ **Important**: Make sure your token has NO trailing spaces or newlines!

4. **Configure Service** (if needed):
   - Service Type: Web Service
   - Start Command: `python main.py` (auto-detected from railway.toml)
   - Port: $PORT (auto-configured)

## 📋 Environment Variables

| Variable | Description | Required | Example |
|----------|-------------|----------|---------|
| `TELEGRAM_TOKEN` | Bot token from @BotFather | ✅ Yes | `123456789:ABC-DEF1234ghIkl...` |
| `PORT` | Server port (auto-set by Railway) | ❌ No | `3000` |
| `ENVIRONMENT` | Environment flag | ❌ No | `production` |

## 🛠️ Architecture

### Railway Deployment

The application runs with dual services:
- **HTTP Health Server**: Binds to `$PORT` for Railway health checks
- **Telegram Bot**: Runs concurrently in background thread

```
Railway → HTTP Health Check (Port $PORT) → ✅ Service Healthy
       └→ Telegram Bot (Background) → 🤖 Handles messages
```

### File Structure

```
databot-analytics/
├── main.py              # Railway entry point with health server
├── bot.py               # Telegram bot with data analytics
├── app.py               # Streamlit web interface  
├── bot_runner.py        # Simple bot runner (legacy)
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
├── railway.toml         # Railway deployment config
├── .env.example         # Environment template
└── README.md           # This file
```

## 🔧 Troubleshooting

### Common Issues

#### 1. "Invalid non-printable ASCII character in URL"
**Cause**: TELEGRAM_TOKEN has trailing newlines or spaces
**Fix**: 
- Copy token carefully from @BotFather
- Don't paste with extra whitespace
- Token format: `123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

#### 2. Railway Service Crashes
**Cause**: Service not binding to $PORT
**Fix**: 
- Use `python main.py` as start command
- Ensure railway.toml is present
- Check Railway logs for specific errors

#### 3. Bot Not Responding  
**Cause**: Invalid or missing token
**Fix**:
- Verify token with @BotFather using `/mybots`
- Check Railway environment variables
- Ensure token has no extra characters

#### 4. File Upload Issues
**Mobile**: Use desktop browser or Telegram bot
**Large Files**: Use bot instead of web interface

### Debug Steps

1. **Check Railway Logs**:
   ```bash
   railway logs
   ```

2. **Test Locally**:
   ```bash
   python bot.py
   # Should show: "✅ Bot is ready!"
   ```

3. **Validate Token Format**:
   - Should be exactly 46 characters
   - Format: `[8-10 digits]:[35 characters A-Z, a-z, 0-9, -, _]`

4. **Health Check**:
   ```bash
   curl https://your-app.railway.app/health
   # Should return: {"status": "healthy", ...}
   ```

## 📊 Usage Examples

### Data Analysis Flow

1. **Upload Data**: Send CSV/Excel file to bot
2. **Get Overview**: Automatic summary statistics  
3. **Visualizations**: Charts and graphs generated
4. **Advanced Analysis**: ML clustering, A/B testing
5. **Export**: Download reports and charts

### Supported File Types

- ✅ CSV files (.csv)
- ✅ Excel files (.xlsx, .xls)  
- ✅ JSON files (via web interface)
- ❌ Large files >50MB (use data sampling)

## 🤝 Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes and test locally
4. Commit: `git commit -m "Add feature"`
5. Push: `git push origin feature-name`  
6. Create Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Support

- 📧 Issues: [GitHub Issues](https://github.com/Artisa111/databot-analytics/issues)
- 💬 Telegram: [@maydatabot123_bot](https://t.me/maydatabot123_bot)
- 📖 Docs: Check this README and code comments

---

**Made with ❤️ for data enthusiasts**
# main.py
import subprocess
import sys
import os
import threading
import time
import platform
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Colored output and emoji
import colorama
from colorama import Fore, Style
colorama.init()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Windows encoding setup
if platform.system() == "Windows":
    os.system("chcp 65001 > nul")  # UTF-8 encoding for terminal

def run_bot():
    """Run Telegram bot with error handling - optional and non-fatal"""
    try:
        # Check if telegram token is available
        telegram_token = os.getenv('TELEGRAM_TOKEN')
        if not telegram_token or not telegram_token.strip():
            print(Fore.YELLOW + "⚠️  TELEGRAM_TOKEN not found - skipping bot startup" + Style.RESET_ALL)
            return
        
        print(Fore.CYAN + "🤖 Starting Telegram bot..." + Style.RESET_ALL)
        # Don't use check=True to prevent crashes
        result = subprocess.run([sys.executable, "bot.py"], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(Fore.RED + f"❌ Bot failed to start: {result.stderr}" + Style.RESET_ALL)
            print(Fore.YELLOW + "⚠️  Bot error won't affect web service" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "✅ Bot started successfully" + Style.RESET_ALL)
            
    except Exception as e:
        print(Fore.RED + f"❌ Bot startup error: {e}" + Style.RESET_ALL)
        print(Fore.YELLOW + "⚠️  Bot error won't affect web service" + Style.RESET_ALL)

def run_streamlit():
    """Run Streamlit web service - always runs for Railway"""
    try:
        print(Fore.GREEN + "📊 Starting Streamlit web service..." + Style.RESET_ALL)
        
        # Get port from environment (Railway sets this)
        port = os.getenv('PORT', '8501')
        
        # Railway-compatible Streamlit startup
        cmd = [
            "streamlit", "run", "app.py",
            "--server.port", port,
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ]
        
        print(f"🚀 Starting Streamlit on 0.0.0.0:{port}")
        subprocess.run(cmd)
        
    except Exception as e:
        print(Fore.RED + f"❌ Streamlit startup error: {e}" + Style.RESET_ALL)
        sys.exit(1)  # Only exit if Streamlit fails (main service)

# Main execution
if __name__ == "__main__":
    print(Fore.BLUE + "🚀 DataBot Analytics - Starting services..." + Style.RESET_ALL)
    
    # Start bot in separate thread (optional, non-fatal)
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Give bot a moment to start if token is available
    time.sleep(2)
    
    # Run Streamlit in main thread (required service)
    run_streamlit()
#!/usr/bin/env python3
"""
DataBot Analytics - Resilient Launcher
Starts Streamlit web interface and optionally runs Telegram bot.
Web interface stays alive even if bot fails.
"""

import subprocess
import sys
import os
import threading
import time
import logging
from colorama import Fore, Style, init

# Initialize colorama
init()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run_bot():
    """Run Telegram bot in isolated process - failures won't crash web interface"""
    token = os.getenv('TELEGRAM_TOKEN', '').strip()
    if not token:
        logger.warning(f"{Fore.YELLOW}🤖 No TELEGRAM_TOKEN found - bot will not start{Style.RESET_ALL}")
        logger.info(f"{Fore.CYAN}💡 Set TELEGRAM_TOKEN environment variable to enable bot{Style.RESET_ALL}")
        return
    
    logger.info(f"{Fore.CYAN}🤖 Starting Telegram bot...{Style.RESET_ALL}")
    
    try:
        # Run bot in subprocess - if it crashes, web stays alive
        result = subprocess.run([sys.executable, "bot.py"], 
                              capture_output=True, text=True, timeout=None)
        
        if result.returncode != 0:
            logger.error(f"{Fore.RED}❌ Bot failed with exit code {result.returncode}{Style.RESET_ALL}")
            if result.stderr:
                logger.error(f"Bot stderr: {result.stderr}")
        else:
            logger.info(f"{Fore.GREEN}✅ Bot completed successfully{Style.RESET_ALL}")
            
    except subprocess.TimeoutExpired:
        logger.warning(f"{Fore.YELLOW}⚠️ Bot process timeout{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}❌ Bot error: {e}{Style.RESET_ALL}")

def run_streamlit():
    """Run Streamlit web interface - this is the primary service"""
    port = os.getenv('PORT', '8501')
    
    logger.info(f"{Fore.GREEN}📊 Starting Streamlit web interface on port {port}...{Style.RESET_ALL}")
    
    try:
        # Streamlit command with proper Railway configuration
        cmd = [
            "streamlit", "run", "app.py",
            "--server.port", port,
            "--server.address", "0.0.0.0",
            "--server.headless", "true",
            "--server.enableCORS", "false",
            "--server.enableXsrfProtection", "false"
        ]
        
        # This is the main process - if this fails, the whole app should fail
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        logger.info(f"{Fore.YELLOW}🛑 Streamlit stopped by user{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"{Fore.RED}❌ Streamlit error: {e}{Style.RESET_ALL}")
        raise

def main():
    """Main launcher - Streamlit primary, bot optional"""
    logger.info(f"{Fore.MAGENTA}🚀 DataBot Analytics starting up...{Style.RESET_ALL}")
    
    # Start bot in background thread (non-blocking, can fail safely)
    if os.getenv('TELEGRAM_TOKEN'):
        bot_thread = threading.Thread(target=run_bot, daemon=True, name="TelegramBot")
        bot_thread.start()
        time.sleep(2)  # Give bot time to start
    else:
        logger.info(f"{Fore.CYAN}💡 Skipping bot - no TELEGRAM_TOKEN set{Style.RESET_ALL}")
    
    # Run Streamlit as main process (blocking - this is what Railway monitors)
    run_streamlit()

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Railway-compatible main entry point for DataBot Analytics.
Serves HTTP health check on $PORT while running Telegram bot concurrently.
"""
import os
import threading
import time
import logging
from http.server import HTTPServer, BaseHTTPRequestHandler
from bot import DataAnalyticsBot

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class HealthHandler(BaseHTTPRequestHandler):
    """Simple HTTP health check handler for Railway deployment"""
    
    def do_GET(self):
        if self.path in ['/', '/health']:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            status = {
                'status': 'healthy',
                'service': 'databot-analytics',
                'bot_status': 'running' if bot_status.get('running') else 'stopped'
            }
            self.wfile.write(str(status).encode())
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default HTTP request logging to reduce noise
        pass

def run_bot():
    """Run the Telegram bot in a separate thread"""
    global bot_status
    
    try:
        logger.info("🤖 Starting Telegram bot...")
        bot = DataAnalyticsBot()
        bot_status['running'] = True
        bot.run()
    except ValueError as e:
        logger.error(f"❌ Bot configuration error: {e}")
        logger.info("💡 Check your Railway Variables and ensure TELEGRAM_TOKEN is set correctly")
        logger.info("📝 TELEGRAM_TOKEN should be in format: 123456789:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
        bot_status['running'] = False
    except Exception as e:
        logger.error(f"❌ Unexpected bot error: {e}")
        logger.info("💡 Check your internet connection and bot token!")
        bot_status['running'] = False

def run_health_server():
    """Run HTTP health server for Railway"""
    port = int(os.environ.get('PORT', 3000))
    
    logger.info(f"🌐 Starting health server on 0.0.0.0:{port}")
    
    server = HTTPServer(('0.0.0.0', port), HealthHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("🛑 Health server stopped")
        server.shutdown()

# Global bot status tracker
bot_status = {'running': False}

if __name__ == "__main__":
    logger.info("🚀 Starting DataBot Analytics for Railway deployment")
    
    # Start bot in background thread
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()
    
    # Give bot a moment to initialize
    time.sleep(2)
    
    # Start health server (blocks main thread - Railway needs this)
    try:
        run_health_server()
    except KeyboardInterrupt:
        logger.info("🛑 Shutting down DataBot Analytics")
import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot Configuration
# Do NOT provide any default; only read from environment variables.
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if TELEGRAM_TOKEN in (None, '', 'your_bot_token_here'):
    TELEGRAM_TOKEN = None

# Streamlit Configuration
PAGE_TITLE = "DataBot Analytics"
PAGE_ICON = "📊"
LAYOUT = "wide"

# Colors Theme
COLORS = {
    'primary': '#1f77b4',
    'secondary': '#ff7f0e',
    'success': '#2ca02c',
    'danger': '#d62728',
    'warning': '#ff7f0e',
    'info': '#17a2b8',
    'light': '#f8f9fa',
    'dark': '#343a40'
}
# main.py
import subprocess
import sys
import os
import threading
import time
import platform

# Colored output and emojis
import colorama
from colorama import Fore, Style
colorama.init()

# Encoding setup for Windows terminal
if platform.system() == "Windows":
    os.system("chcp 65001 > nul")  # Use UTF-8 code page in terminal

# Run the bot
def run_bot():
    print(Fore.CYAN + "🤖 Starting bot..." + Style.RESET_ALL)
    subprocess.run([sys.executable, "bot.py"], check=True)

# Run Streamlit
def run_streamlit():
    print(Fore.GREEN + "📊 Starting Streamlit..." + Style.RESET_ALL)
    subprocess.run(["streamlit", "run", "app.py"], check=True)

# Main entrypoint
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)

    bot_thread.start()
    time.sleep(2)  # Give the bot a moment to start
    streamlit_thread.start()

    bot_thread.join()
    streamlit_thread.join()
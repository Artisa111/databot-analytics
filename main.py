# main.py
import subprocess
import sys
import os
import threading
import time
import platform

# Цветной вывод и эмодзи
import colorama
from colorama import Fore, Style
colorama.init()

# Настройка кодировки для Windows
if platform.system() == "Windows":
    os.system("chcp 65001 > nul")  # UTF-8 кодировка в терминале

# Запуск бота
def run_bot():
    print(Fore.CYAN + "🤖 Запуск бота..." + Style.RESET_ALL)
    subprocess.run([sys.executable, "bot.py"], check=True)

# Запуск Streamlit
def run_streamlit():
    print(Fore.GREEN + "📊 Запуск Streamlit..." + Style.RESET_ALL)
    subprocess.run(["streamlit", "run", "app.py"], check=True)

# Основной запуск
if __name__ == "__main__":
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    streamlit_thread = threading.Thread(target=run_streamlit, daemon=True)

    bot_thread.start()
    time.sleep(2)  # Даем боту немного времени на старт
    streamlit_thread.start()

    bot_thread.join()
    streamlit_thread.join()
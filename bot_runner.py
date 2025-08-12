import os 
from bot import DataAnalyticsBot 
 
if __name__ == "__main__": 
    bot = DataAnalyticsBot() 
    print("Bot started!") 
    bot.application.run_polling() 

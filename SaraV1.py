import telebot
import requests
from datetime import datetime

# Initialize the bot with your Telegram bot token
bot = telebot.TeleBot('7615482628:AAFJJylYvg_NDTPFcsw8wxNDJuQjGpSbiu4')

# Command to start the bot
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'Hi! Use /info to get the current date and time, cryptocurrency prices, and local news.')

# Command to get the current date and time, cryptocurrency prices, and local news
@bot.message_handler(commands=['info'])
def send_info(message):
    # Get current date and time
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Get cryptocurrency prices in BRL
    url = 'https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,solana,tether&vs_currencies=brl'
    response = requests.get(url).json()
    btc_price = response['bitcoin']['brl']
    sol_price = response['solana']['brl']
    usdt_price = response['tether']['brl']

    # Get local news from Baixada Fluminense
    news_url = 'https://newsapi.org/v2/everything?q=Baixada%20Fluminense&apiKey=c403f51b14f546fb873070911f675ce2'
    news_response = requests.get(news_url).json()
    articles = news_response['articles'][:5]
    news_message = ''
    for article in articles:
        news_message += f"{article['title']}\n{article['description']}\n{article['url']}\n\n"

    # Create the final message
    final_message = (f"Current date and time: {now}\n\n"
                     f"Bitcoin (BTC): R${btc_price}\n"
                     f"Solana (SOL): R${sol_price}\n"
                     f"USDT (Tether): R${usdt_price}\n\n"
                     f"Local News from Baixada Fluminense:\n{news_message}")

    bot.reply_to(message, final_message)

# Start polling for commands
bot.polling()

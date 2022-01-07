import scraper
import os
import telebot
from telebot.types import BotCommand

# ChannelCondenser_bot
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
  BotCommand('start', 'Starts the bot'),
  #BotCommand('test', 'test')
])

@bot.message_handler(commands=['start'])
def start(message):
    """
  Command that welcomes the user and configures the initial setup
  """

    if message.chat.type == 'private':
      chat_user = message.chat.first_name
    else:
      chat_user = message.chat.title
    
    message_text = f'Hello {chat_user}, Telegram Channel Condenser is now running.'

    bot.reply_to(message, message_text)

@bot.message_handler(commands=['parrot'])
def parrot(message):
    """
  Command that replies the user with the text message it receives
  """

    # Retrieve text
    message_text = message.text
    print('Received message:', message_text)

    bot.reply_to(message, message_text)

    pass


#bot.infinity_polling()
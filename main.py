import scraper
import os
import telebot
from telebot.types import BotCommand
from database import channels

# ChannelCondenser_bot
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
  BotCommand('start', 'Starts the bot'),
  BotCommand('addchannel', 'Adds Channel to subscription list'),
  BotCommand('viewchannel', 'View Currently Subscribed Channels')
])

@bot.message_handler(commands=['start'])
def start(message):
  """
  Command that welcomes the user and configures the initial setup
  """
  chat_id = message.chat.id

  if message.chat.type == 'private':
    chat_user = message.chat.first_name
  else:
    chat_user = message.chat.title
  
  message_text = f'Hello {chat_user}, Telegram Channel Condenser is now running.'

  # Initialise Cart
  channels[chat_id] = dict()

  bot.reply_to(message, message_text)    

def request_start(chat_id):
  """
  Helper function to request user to execute command /start
  """
  if chat_id not in channels:
      bot.send_message(chat_id=chat_id,
                        text='Please start the bot by sending /start')

  return

@bot.message_handler(commands=['addchannel'])
def add_channel(message):
  """
  Command that adds channel to Channels list
  """
  chat_id = message.chat.id

  if chat_id not in channels:
    request_start(chat_id)
    return
  sent = bot.reply_to(message, "Type the channel handle that you would like to subscribe to. E.g. sgjobspoint")
  bot.register_next_step_handler(sent, add_channel_name)
  #pass


def add_channel_name(message):
  channels[message.chat.id][message.text] = 2
  print(channels)

@bot.message_handler(commands=['initialize'])
def initialize(message):
#Retrieve list of channels & find the last messages
  """
  Command that initialize channel to latest message id
  """
  chat_id = message.chat.id

  if chat_id not in channels:
    request_start(chat_id)
    return
  
  if(channels[message.chat.id]):
    for group_name in channels[message.chat.id]:
      #THRESHOLD = len(scraper.get_html(group_name, 1))
      print("message_details below")
      print(channels)
      last_message = scraper.scrape(channels)
      print(last_message)

@bot.message_handler(commands=['getupdate'])
def get_update(message):

  chat_id = message.chat.id

  if chat_id not in channels:
    request_start(chat_id)
    return

  if(channels[message.chat.id]):
    for group_name in channels[message.chat.id]:
      number = channels[message.chat.id][group_name] # 22
      print("message_details below")
      print(channels)
      msg_list = scraper.get_update(channels, number)
      for i in msg_list:
        if i == 0:
          i = "No new Updates"
        bot.send_message(
        chat_id = chat_id,
        text = i,
        #parse_mode = 'MarkdownV2'
        parse_mode = 'HTML'
      )





@bot.message_handler(commands=['viewchannel'])
def view_channels(message):
  """
  Command that adds channel to Channels list
  """
  chat_id = message.chat.id

  if chat_id not in channels:
    request_start(chat_id)
    return

  channels_text = '__Channels Subscribed__\n'

  print(channels) #weird
  if(channels[message.chat.id]):
    for channel_id in channels[message.chat.id]:
      channels_text += f'@{channel_id}\n'
  else:
    channels_text = 'No Channels Subscribed to currently'
  
  bot.send_message(
    chat_id = chat_id,
    text = channels_text,
    parse_mode = 'MarkdownV2'
  )

bot.infinity_polling()
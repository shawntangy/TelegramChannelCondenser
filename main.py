import scraper
import os
import telebot
from telebot.types import BotCommand
from database import channels, past_messages

# ChannelCondenser_bot
API_KEY = os.getenv('API_KEY')

bot = telebot.TeleBot(API_KEY)

bot.set_my_commands([
    BotCommand('start', 'Starts the bot'),
    BotCommand('addchannel', 'Adds Channel to subscription list'),
    BotCommand('viewchannel', 'View Currently Subscribed Channels'),
    BotCommand('initialize', 'Initialize and retrieve up to latest feed'),
    BotCommand('getupdate', 'Update to latest feed'),
    BotCommand('clear', 'removes all channels from the list')
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
    past_messages[chat_id] = dict()
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
    # pass


def add_channel_name(message):
    channels[message.chat.id][message.text] = 2
    print(channels)


@bot.message_handler(commands=['initialize'])
def initialize(message):
    # Retrieve list of channels & find the last messages
    """
    Command that initialize channel to latest message id
    """
    chat_id = message.chat.id

    if chat_id not in channels:
        request_start(chat_id)
        return

    bot.reply_to(message, "Initializing, please wait")

    if (channels[message.chat.id]):
        # for group_name in channels[message.chat.id]:
        # print(group_name)
        # THRESHOLD = len(scraper.get_html(group_name, 1))
        print("message_details below")
        print(channels)
        scraper.scrape(channels)
        # print(last_message)

    bot.send_message(
        chat_id=chat_id,
        text="Initialization Done"
    )


@bot.message_handler(commands=['getupdate'])
def get_update(message):
    chat_id = message.chat.id

    if chat_id not in channels:
        request_start(chat_id)
        return

    if not (channels[message.chat.id]):
        channels_text = 'No Channels Subscribed to currently'

        bot.send_message(
            chat_id=chat_id,
            text=channels_text,
            parse_mode='MarkdownV2'
        )

        return

    if (channels[message.chat.id]):
        # for group_name in channels[message.chat.id]:
        # number = channels[message.chat.id][group_name] # 22
        print("message_details below")
        print(channels)
        msg_list = scraper.get_update(channels)
        print(msg_list)

        content = "<b>Here are your messages:</b> \n\n"
        for j in range(len(msg_list)):
            for i in range(1, len(msg_list[j])):

                if msg_list[j][i] == 0:
                    content += "No new Updates" + " from " + msg_list[j][0] + "\n\n"
                else:
                    content += "From " + msg_list[j][0] + ": " + msg_list[j][i] + "\n\n"
        bot.send_message(
            chat_id=chat_id,
            text=content,
            # parse_mode = 'MarkdownV2'
            parse_mode='HTML'
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

    print(channels)  # weird
    if (channels[message.chat.id]):
        for channel_id in channels[message.chat.id]:
            channels_text += f'@{channel_id}\n'
    else:
        channels_text = 'No Channels Subscribed to currently'

    bot.send_message(
        chat_id=chat_id,
        text=channels_text,
        parse_mode='MarkdownV2'
    )


@bot.message_handler(commands=['clear'])
def clear_channels(message):
    """
    Command that removes all channels from the list
    """

    chat_id = message.chat.id
    if chat_id not in channels:
        request_start(chat_id)
        return

    channel_cleared_text = 'Channel list cleared!'
    channels[chat_id].clear()

    bot.send_message(chat_id=chat_id, text=channel_cleared_text)


bot.infinity_polling()


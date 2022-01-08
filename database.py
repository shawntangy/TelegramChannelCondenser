'''
A database storing the cart for each chat.
list {
  chat_id: {
    channel_id: post_id
  }
}
'''
channels = {}
past_messages = {}
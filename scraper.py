import schedule
import requests
from bs4 import BeautifulSoup

message_details = {"user1":
                       {"SGBIGPURCHASES": 2}
                   }

# to retrieve initial source code length
def get_html(group_name, number):
    url = "https://t.me/" + group_name + "/" + str(number)
    response = requests.get(url)
    html = response.text
    return html

# to retrieve actual content
def scrape(message_details):
    for i in message_details:
        for key, value in message_details[i].items():
            group_name = key
            last_message = value
            return poll(message_details, i, group_name, last_message)

def poll(message_details, i, group_name, last_message):
  while True:
    html = get_html(group_name, last_message)
    if (len(html) - THRESHOLD >= 2000):
        soup = BeautifulSoup(html, "html.parser")

        # to print message content
        message = str(soup.select_one("meta[property=\"og:description\"]"))
        # removes first 15 char, last 29
        message = message[15:-29]

        print(message)
        # print(type(message))
        last_message += 1
        print("last message 39")
        print(last_message)
        # INCREMENT BACK INTO DICTIONARY NOT DONE
    else:
      for j in range(5):
        if (len(get_html(group_name, last_message + j + 1)) - THRESHOLD < 2000):
          print("checking last_message +"+ str(j+1))
          pass
        else: #to enter this - a message must exist
          # this will be an actual message, hence update last_message
          last_message = last_message + j + 1
          message_details[i][group_name] = last_message 
          print("scan complete, returning latest number")
          return last_message
      return last_message
    message_details[i][group_name] = last_message 


THRESHOLD = len(get_html("SGBIGPURCHASES", 1))

last_message = scrape(message_details)

schedule.every(5).seconds.do(scrape, message_details)

last_message = scrape(message_details)

while True:
  schedule.run_pending()


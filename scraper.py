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

# to retrieve message from html
def get_msg(html):
  soup = BeautifulSoup(html, "html.parser")
  message = str(soup.select_one("meta[property=\"og:description\"]"))
  # removes first 15 char, last 29
  message = message[15:-29]
  return message

# to retrieve actual content
def scrape(message_details):
  print("entered scrape")
  for i in message_details:
      for key, value in message_details[i].items():
          group_name = key
          last_message = value
          message = poll(message_details, i, group_name, last_message)
          while (message != 0):
            message = poll(message_details, i, group_name, message_details[i][group_name])
          return get_msg(get_html(group_name, message_details[i][group_name]- 1))
      

def poll(message_details, user, group_name, number):
  html = get_html(group_name, number)
  
  if (len(html) - THRESHOLD >= 2000): #means valid message
    print(number," is valid")
    number += 1
    message_details[user][group_name] = number
    # format content and return
    return get_msg(html)

  else:
    # Fails means check next 5 if deleted
    print("entered else")
    for j in range(5):
      print(j)
      if (len(get_html(group_name, number + j + 1)) - THRESHOLD >= 2000):
        number = number + j + 1
        message_details[user][group_name] = number
        html = get_html(group_name, number)
        return get_msg(html)
    
    print("already latest")
    return 0


THRESHOLD = len(get_html("SGBIGPURCHASES", 1))

schedule.every(5).seconds.do(scrape, message_details)

last_message = scrape(message_details)

while True:
  schedule.run_pending()
  #print(last_message)


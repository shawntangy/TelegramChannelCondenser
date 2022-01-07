import schedule
import requests
from bs4 import BeautifulSoup

message_details = {"user1":
                       {"SGBIGPURCHASES": 2}
                   }


def base_length(group_name):
    url = "https://t.me/" + group_name + "/1"
    response = requests.get(url)
    html = response.text
    return len(html)


def scrape(message_details):
    for i in message_details:
        for key, value in message_details[i].items():
            group_name = key
            last_message = value
    while True:
        url = "https://t.me/" + group_name + "/" + str(last_message)
        response = requests.get(url)
        html = response.text

        if (len(html) - THRESHOLD >= 2000):
            soup = BeautifulSoup(html, "html.parser")

            # to print message content
            message = str(soup.select_one("meta[property=\"og:description\"]"))
            # removes first 15 char, last 29
            message = message[15:-29]

            print(message)
            # print(type(message))
            last_message += 1

        else:
            print("hello")
            return last_message


THRESHOLD = base_length("SGBIGPURCHASES")

for i in message_details:
    for key, value in message_details[i].items():
        print(value)

last_message = scrape(message_details)

schedule.every(5).seconds.do(scrape, message_details)

last_message = scrape(message_details)

for i in message_details:
    for key, value in message_details[i].items():
        print(value)

while True:
    schedule.run_pending()

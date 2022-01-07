import schedule
import requests
from bs4 import BeautifulSoup

last_message = 2


def base_length(group_name):
    url = "https://t.me/" + group_name + "/1"
    response = requests.get(url)
    html = response.text
    return len(html)


def scrape(group_name, last_message):
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

print(last_message)

last_message = scrape("SGBIGPURCHASES", last_message)

schedule.every(5).seconds.do(scrape, "SGBIGPURCHASES", last_message)

last_message = scrape("SGBIGPURCHASES", last_message)

print(last_message)

while True:
    schedule.run_pending()

print(list(message_details.keys())[0])
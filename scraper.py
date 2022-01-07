import requests
from bs4 import BeautifulSoup

url = "https://t.me/SGResearchLobang/991"
#url = "https://t.me/sgjobspoint/356"

response = requests.get(url)
html = response.text
#print(html)
#print(len(html))

soup = BeautifulSoup(html, "html.parser")

# to print message content
message = str(soup.select_one("meta[property=\"og:description\"]"))
# removes first 15 char, last 29
message = message[15:-29]

print(message)
print(type(message))


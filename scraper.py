from database import past_messages
import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher


# message_details = {"user1":
# {"SGBIGPURCHASES": 2}
# }

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
    pstmsg = []
    print("entered scrape")
    for i in message_details:
        for key, value in message_details[i].items():
            group_name = key
            THRESHOLD = len(get_html(group_name, 1))
            last_message = value
            message = poll(message_details, i, group_name, last_message, THRESHOLD)
            pstmsg.append(message)
            while (message != 0):
                message = poll(message_details, i, group_name, message_details[i][group_name], THRESHOLD)
                pstmsg.append(message)

    past_messages[i] = pstmsg


def similarity(msg_list, tmp_list, user):
    for j in range(len(msg_list)):
        for i in range(1, len(msg_list[j])):
            a = msg_list[j][i]
            if (a != 0):
                for k in past_messages[user]:
                    if (SequenceMatcher(None, str(a), str(k)).ratio() > 0.8):
                        msg_list[j][i] = 0
                        tmp_list.pop()
    return tmp_list


def get_update(message_details):
    print("entered update")
    msg_list = []
    for i in message_details:
        tmp_list = past_messages[i]
        for key, value in message_details[i].items():
            group_name = key
            THRESHOLD = len(get_html(group_name, 1))
            last_message = value
            message = poll(message_details, i, group_name, last_message, THRESHOLD)
            msg_list.append([group_name, message])
            tmp_list.append(message)
            while (message != 0):
                message = poll(message_details, i, group_name, message_details[i][group_name], THRESHOLD)
                print("message here")
                print(message)
                if (message != 0):
                    msg_list.append([group_name, message])
                    tmp_list.append(message)
            print("msg_list here1")
            print(msg_list)
            # msg_list.pop()
            tmp_list = similarity(msg_list, tmp_list, i)
            print("msg_list here2")
            print(msg_list)
            print("tmp_list below")
            print(tmp_list)
            past_messages[i] = tmp_list
        return msg_list


def poll(message_details, user, group_name, number, THRESHOLD):
    html = get_html(group_name, number)

    if (len(html) - THRESHOLD >= 2000):  # means valid message
        print(number, " is valid")
        number += 1
        print("user and group_name below")
        print(user, group_name)
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

# THRESHOLD = len(get_html("SGBIGPURCHASES", 1))

# schedule.every(5).seconds.do(scrape, message_details)

# last_message = scrape(message_details)

# while True:
# schedule.run_pending()
# print(last_message)



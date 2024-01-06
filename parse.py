import re
import time
from fake_useragent import UserAgent
import requests


def generate_user_agent():
    user_agent = UserAgent()
    random_user_agent = user_agent.random

    print(random_user_agent)

    return {'User-Agent': random_user_agent}

def parse(name):
    name_id_response = requests.get(f"https://steamcommunity.com/market/listings/730/{name}", headers=generate_user_agent())
    name_id = re.search(r"Market_LoadOrderSpread\( (?P<item_id>\d+) \)", name_id_response.text).group("item_id")

    time.sleep(1)

    response = requests.get(f"https://steamcommunity.com/market/itemordershistogram?country=US&"
                            f"language=russian&currency=5&item_nameid={name_id}&two_factor=0", headers=generate_user_agent()).json()

    return int(response["highest_buy_order"]) / 100, int(response["lowest_sell_order"]) / 100


if __name__ == '__main__':
    with open('skins.txt', 'r', encoding='utf-8') as f:
        data = f.readlines()

    for name in data:
        print(name[:-1])
        print(parse(name[:-1]))

        time.sleep(1)

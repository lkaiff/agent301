import requests
from bots.agent301.strings import HEADERS

def get_info(farmer):
    url = "https://api.agent301.org/getMe"
    payload = {"referrer_id": 0}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        balance = data["result"]["balance"]
        ticket = data["result"]["tickets"]
        farmer.log(f"Balance: {balance:,} - Available ticket: {ticket:,}")
        return ticket
    else:
        farmer.log(f"Ошибка при получении информации об аккаунте: {response.status_code}")
        return None

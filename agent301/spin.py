import requests
from bots.agent301.strings import HEADERS
from bots.agent301.info import get_info

def spin(farmer):
    url = "https://api.agent301.org/wheel/spin"
    payload = {}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        farmer.log(f"Ошибка при запуске колеса: {response.status_code}")
        return None

def process_spin_wheel(farmer):
    while True:
        ticket = get_info(farmer)
        if ticket is not None:
            if ticket > 0:
                start_spinning = spin(farmer)
                if start_spinning:
                    status = start_spinning["ok"]
                    if status:
                        reward = start_spinning["result"]["reward"]
                        balance = start_spinning["result"]["balance"]
                        toncoin = start_spinning["result"]["toncoin"]
                        notcoin = start_spinning["result"]["notcoin"]
                        tickets = start_spinning["result"]["tickets"]

                        farmer.log(f"Auto Spin Wheel: Success | Reward: {reward} - Balance: {balance:,} - Toncoin: {toncoin:,} - Notcoin: {notcoin:,} - Tickets: {tickets:,}")
                    else:
                        farmer.log("Auto Spin Wheel: Fail")
                        break
                else:
                    break
            else:
                farmer.log("Auto Spin Wheel: No ticket available")
                break
        else:
            farmer.log("Auto Spin Wheel: Ticket data not found!")
            break

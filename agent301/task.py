import requests
from bots.agent301.strings import HEADERS

def get_task(farmer):
    url = "https://api.agent301.org/getTasks"
    payload = {}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        task_list = data["result"]["data"]
        return task_list
    else:
        farmer.log(f"Ошибка при получении списка заданий: {response.status_code}")
        return None

def do_task(farmer, task_type):
    url = "https://api.agent301.org/completeTask"
    payload = {"type": task_type}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        status = data["result"]["is_completed"]
        return status
    else:
        farmer.log(f"Ошибка при выполнении задания: {response.status_code}")
        return None

def process_do_task(farmer):
    task_list = get_task(farmer)
    if task_list:
        for task in task_list:
            task_type = task["type"]
            task_name = task["title"]
            task_status = task["is_claimed"]
            if task_status:
                farmer.log(f"{task_name}: Completed")
            else:
                if task_type == "video":
                    count = task["count"]
                    max_count = task["max_count"]
                    for i in range(max_count - count):
                        do_task_status = do_task(farmer, task_type)
                        if do_task_status:
                            farmer.log(f"{task_name}: Success")
                        else:
                            farmer.log(f"{task_name}: Incomplete")
                else:
                    do_task_status = do_task(farmer, task_type)
                    if do_task_status:
                        farmer.log(f"{task_name}: Success")
                    else:
                        farmer.log(f"{task_name}: Incomplete")
    else:
        farmer.log("Auto Do Task: Task list not found!")

def get_wheel_task(farmer):
    url = "https://api.agent301.org/wheel/load"
    payload = {}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        task_list = data["result"]["tasks"]
        return task_list
    else:
        farmer.log(f"Ошибка при получении списка заданий колеса: {response.status_code}")
        return None

def do_wheel_task(farmer, type):
    url = "https://api.agent301.org/wheel/task"
    payload = {"type": type}
    response = farmer.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        status = data["ok"]
        return status
    else:
        farmer.log(f"Ошибка при выполнении задания колеса: {response.status_code}")
        return None

def process_do_wheel_task(farmer):
    wheel_task = get_wheel_task(farmer)
    if wheel_task:
        for type in wheel_task.keys():
            while True:
                do_wheel_task_status = do_wheel_task(farmer, type)
                if do_wheel_task_status:
                    farmer.log(f"Auto Do Wheel Task: Check status | Type: {type} - Status: Success")
                else:
                    farmer.log(f"Auto Do Wheel Task: Check status | Type: {type} - Status: Not available")
                    break
    else:
        farmer.log("Auto Do Wheel Task: Task list not found!")

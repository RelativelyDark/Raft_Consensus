import sys
import requests


def get_all_tasks(addr):
    try:
        response = requests.get(addr)
        if response.status_code == 200:
            tasks = response.json()
            for task in tasks:
                print(task)
        else:
            print("Error: Unable to retrieve tasks")
            print("Response status code:", response.status_code)
            print("Response content:", response.content)
    except Exception as e:
        print("An error occurred:", e)

def get_task(addr, task_id):
    try:
        response = requests.get(f"{addr}/{task_id}")
        if response.status_code == 200:
            task = response.json()
            print(task)
        else:
            print("Error: Unable to retrieve task")
            print("Response status code:", response.status_code)
            print("Response content:", response.content)
    except Exception as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        addr = sys.argv[1] + "/tasks"
        get_all_tasks(addr)
    elif len(sys.argv) == 3:
       
        addr = sys.argv[1]
        task_id = sys.argv[2]
        get_task(addr, task_id)
    else:
        print("Usage: python client.py http://localhost:5000")

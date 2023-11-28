import requests
import time
from datetime import datetime, timedelta

url = "http://10.244.0.17:32186/api/recommender"
headers = {"Content-Type": "application/json"}
data = {"songs": ["Caroline", "HUMBLE."]}
duration_minutes = 6
interval_seconds = 1
output_file = "syncTime.txt"

start_time = datetime.now()
end_time = start_time + timedelta(minutes=duration_minutes)

with open(output_file, "w") as file:
    while datetime.now() < end_time:
        request_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        response = requests.post(url, json=data, headers=headers)
        response_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        file.write(f"Request Sent: {request_time}\n")
        file.write(f"Response Received: {response.text}\n")
        file.write(f"Response Time: {response_time}\n")
        file.write("\n")

        time.sleep(interval_seconds)
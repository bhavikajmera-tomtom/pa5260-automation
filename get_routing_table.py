import requests, urllib3, os
from dotenv import load_dotenv
load_dotenv()
urllib3.disable_warnings()

HOSTNAME = os.getenv("PANOS_HOSTNAME")
API_KEY = os.getenv("PANOS_API_KEY")

url = f"https://{HOSTNAME}/api/"
params = {
    "type": "op",
    "cmd": "<show><routing><route></route></routing></show>",
    "key": API_KEY
}
response = requests.get(url, params=params, verify=False)
print(response.text)
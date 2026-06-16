import requests, urllib3
urllib3.disable_warnings()

HOSTNAME = "10.21.129.28"
API_KEY = "LUFRPT1Sczg3V3IzdmF3U0JtME1hbWQvanhuaUxaU0E9ZlJjZG5SUitSWnU1M1A5ejRvVG5SUWFPSDJhMDdiWWgwSktKRzA2WDJHSGx5bmpiSEU5dnBUWXM1bmoxaW50aXdnMVBjUlNsazJDVXpQN282WGo4SVE9PQ=="

url = f"https://{HOSTNAME}/api/"
params = {
    "type": "op",
    "cmd": "<show><routing><route></route></routing></show>",
    "key": API_KEY
}
response = requests.get(url, params=params, verify=False)
print(response.text)
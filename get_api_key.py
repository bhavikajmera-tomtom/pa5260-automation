import requests, urllib3, os, sys, xml.etree.ElementTree as ET
from dotenv import load_dotenv
load_dotenv()
urllib3.disable_warnings()

HOSTNAME = os.getenv("PANOS_HOSTNAME")

if not HOSTNAME:
    print("Error: PANOS_HOSTNAME not set in .env")
    sys.exit(1)

username = input("Username: ")
password = input("Password: ")

url = f"https://{HOSTNAME}/api/"
params = {
    "type": "keygen",
    "user": username,
    "password": password
}

response = requests.get(url, params=params, verify=False)
root = ET.fromstring(response.text)

if root.attrib.get("status") == "success":
    key = root.find(".//key").text
    print(f"\nAPI Key: {key}")
    print("\nAdd this to your .env file:")
    print(f"PANOS_API_KEY={key}")
else:
    msg = root.find(".//msg")
    print(f"Error: {msg.text if msg is not None else response.text}")
    sys.exit(1)

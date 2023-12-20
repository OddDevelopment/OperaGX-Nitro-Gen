import requests
import json
import time

# ---
# Coded by Odd!
# Github: https://github.com/OddDevelopment/OperaGX-Nitro-Gen
# Portfolio: https://odd.gay
# ---

url = 'https://api.discord.gx.games/v1/direct-fulfillment'
headers = {
    'authority': 'api.discord.gx.games',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    'origin': 'https://www.opera.com',
    'referer': 'https://www.opera.com/',
    'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
}

data = {
    'partnerUserId': '50b1bf177eca2a06f77680c1aa6277e1d5a44eb6d8b4a72545348e4828cf0753'
}

while True:
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        token = json.loads(response.text)['token']
        with open('codes.txt', 'a') as file:
            file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
        print("Token saved to codes.txt file.")
    else:
        print(f"Request failed with status code {response.status_code}.")
        print(f"Error message: {response.text}")
    time.sleep(1)

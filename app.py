import requests
import json
import time
import random
import string


# ---
# Coded by Odd!
# Contributers: DuckyBlender and NorthernChicken and NotClavilux
# Github: https://github.com/OddDevelopment/OperaGX-Nitro-Gen
# Portfolio: https://odd.gay
# ---


URL = 'https://api.discord.gx.games/v1/direct-fulfillment'
HEADERS = {
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


def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def save_token_to_file(token):
    with open('codes.txt', 'a') as file:
        file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n\n")

def get_proxies_from_file(filename='proxies.txt'):
    with open(filename, 'r') as file:
        proxies = file.read().splitlines()
    return proxies

def perform_request(session, url, headers, data, proxy):
    try:
        response = session.post(url, headers=headers, json=data, proxies={'http': f'http://{proxy}'}, timeout=10)
        return response
    except Exception as e:
        print(f"Request failed: {str(e)}")
        return None


if __name__ == "__main__":
    proxies = get_proxies_from_file()
    session = requests.Session()

    try:
        for proxy in proxies:
            response = perform_request(session, URL, HEADERS, {'partnerUserId': generate_random_string(64)}, proxy)

            if response and response.status_code == 200:
                token = response.json().get('token', '')
                save_token_to_file(token)
                print("Token saved to codes.txt file.")
            elif response and response.status_code == 429:
                print("Rate limit exceeded! Waiting one minute to allow for cooldown.")
                time.sleep(60)
            elif response and response.status_code == 504:
                print("Server timed out! Trying again in 5 seconds.")
                time.sleep(5)
            else:
                if response:
                    print(f"Request failed with status code {response.status_code}.")
                    print(f"Error message: {response.text}")
                else:
                    print("No response received.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        session.close()

import requests
import random
import threading
import time
from datetime import datetime

# Function to generate random proxy
def generate_proxy():
    ip = "{}".format(".".join(map(str, (random.randint(1, 255) for _ in range(4)))))
    port = random.randint(1024, 65535)
    return f"{ip}:{port}"

# Function to check if a proxy is live
def check_proxy(proxy, test_url="http://www.google.com"):
    try:
        response = requests.get(test_url, proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=10)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Function to save live proxy to file
def save_live_proxy(proxy, filename="liveproxy.txt"):
    try:
        with open(filename, 'r+') as file:
            existing_proxies = set(line.strip() for line in file.readlines())
            if proxy not in existing_proxies:
                file.write(f"{proxy}\n")
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write(f"{proxy}\n")

# Main function for proxy generation and checking
def generate_and_check_proxies(target_live_proxies):
    live_count = 0
    generated_count = 0

    print(f"[INFO] Starting proxy generator. Target: {target_live_proxies} live proxies.")

    while live_count < target_live_proxies:
        proxy = generate_proxy()
        generated_count += 1

        print(f"[INFO] Checking generated proxy: {proxy}")
        if check_proxy(proxy):
            save_live_proxy(proxy)
            live_count += 1
            print(f"[LIVE] Proxy {proxy} is live. Saved to liveproxy.txt. ({live_count}/{target_live_proxies})")
        else:
            print(f"[DEAD] Proxy {proxy} is dead.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[INFO] Generated proxies: {generated_count} | Live proxies: {live_count} | Time: {timestamp}")

    print(f"[DONE] Target of {target_live_proxies} live proxies reached.")

# Entry point
if __name__ == "__main__":
    try:
        target_live = int(input("Enter the number of live proxies to generate: "))
        generate_and_check_proxies(target_live)
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number.")

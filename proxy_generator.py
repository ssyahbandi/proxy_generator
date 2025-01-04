import random
import requests
import time
from colorama import Fore, Style, init

# Initialize colorama
init()

# Function to generate random proxy
def generate_proxy():
    """Generates a random proxy in the format IP:Port"""
    ip = ".".join(str(random.randint(1, 255)) for _ in range(4))
    port = random.randint(1000, 65535)
    return f"{ip}:{port}"

# Function to check if a proxy is live
def check_proxy(proxy, test_url="http://www.google.com"):
    """Checks if the proxy is live by making a request"""
    try:
        response = requests.get(test_url, proxies={"http": f"http://{proxy}", "https": f"https://{proxy}"}, timeout=5)
        if response.status_code == 200:
            return True
    except requests.exceptions.RequestException:
        pass
    return False

# Function to save live proxies avoiding duplicates
def save_live_proxy(proxy, filename="liveproxy.txt"):
    """Saves the live proxy to a file, avoiding duplicates"""
    try:
        with open(filename, 'a+') as file:
            file.seek(0)
            existing_proxies = set(line.strip() for line in file.readlines())
            if proxy not in existing_proxies:
                file.write(f"{proxy}\n")
    except Exception as e:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Error saving proxy: {e}")

# Main function to run the proxy generator
def run_proxy_generator(target_live_proxies):
    """Generates and checks proxies until the target number of live proxies is reached"""
    generated_count = 0
    live_count = 0

    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} Starting proxy generator. Target: {target_live_proxies} live proxies.")

    while live_count < target_live_proxies:
        proxy = generate_proxy()
        generated_count += 1
        current_time = time.strftime("%H:%M:%S")
        current_date = time.strftime("%Y-%m-%d")

        print(f"{Fore.BLUE}[INFO]{Style.RESET_ALL} [{current_time}] [{current_date}] Checking generated proxy: {proxy}")

        if check_proxy(proxy):
            save_live_proxy(proxy)
            live_count += 1
            print(f"{Fore.GREEN}[LIVE] ✅ [{current_time}] [{current_date}] Proxy {proxy} is live. Total live: {live_count}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}[DEAD] ❌ [{current_time}] [{current_date}] Proxy {proxy} is dead.{Style.RESET_ALL}")

    print(f"{Fore.CYAN}[INFO]{Style.RESET_ALL} [{current_time}] [{current_date}] Proxy generation complete. Generated: {generated_count}, Live: {live_count}.")

# Program execution
if __name__ == "__main__":
    try:
        target = int(input(f"{Fore.YELLOW}Enter the number of live proxies to generate: {Style.RESET_ALL}"))
        run_proxy_generator(target)
    except ValueError:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Please enter a valid number.")

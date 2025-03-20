import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
import logging
from datetime import datetime

logging.basicConfig(
    filename="crypto_parser.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

csv_filename = "cryptocurrencies_history.csv"

if not os.path.exists("user_agents.txt"):
    print("File user_agents.txt not found. Using default User-Agent.")
    user_agents = ["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"]
else:
    with open("user_agents.txt", "r") as file:
        user_agents = file.readlines()

user_agent = random.choice(user_agents).strip()
headers = {"User-Agent": user_agent}

url = "https://finance.ua/ua/crypto"

try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.RequestException as e:
    logging.error(f"Error while retrieving data: {e}")
    print(f"Error while retrieving data: {e}")
    exit(1)

soup = BeautifulSoup(response.text, "html.parser")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

coins = []
for code_tag, name_tag, price_tag in zip(
        soup.find_all("p", class_="CoinsListstyles__Code-sc-1c8245s-24 lgioIM"),
        soup.find_all("p", class_="CoinsListstyles__Name-sc-1c8245s-23 kVPjIs"),
        soup.find_all("td", class_="CoinsListstyles__Price-sc-1c8245s-25 fYNuHQ")):
    try:
        code = code_tag.get_text(strip=True)
        name = name_tag.get_text(strip=True)
        price_text = price_tag.get_text(strip=True)
        price = float(re.sub(r"[^\d.,]", "", price_text).replace(",", "."))
        coins.append((code, name, price))
    except (ValueError, AttributeError) as e:
        logging.warning(f"Error while processing data: {e}")

if not coins:
    logging.warning("Failed to retrieve data. Check the HTML structure of the site.")
    print("Parsing error. The site may have changed.")
    exit(1)

coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

header_needed = not os.path.isfile(csv_filename) or os.stat(csv_filename).st_size == 0

with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    if header_needed:
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price ($)"])
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([timestamp, index, coin[1], coin[0], coin[2]])

logging.info(f"Successfully saved {len(coins_sorted[:10])} records in {csv_filename}.")
print(f"Saving data in '{csv_filename}'.")
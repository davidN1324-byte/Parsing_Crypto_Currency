import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
from datetime import datetime

# File for saving history
csv_filename = "cryptocurrencies_history.csv"

# Reading User-Agents
with open("user_agents.txt", "r") as file:
    user_agents = file.readlines()

user_agent = random.choice(user_agents).strip()  

headers = {"User-Agent": user_agent}

url = "https://finance.ua/ua/crypto"
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

coins = []
for code_tag, name_tag, price_tag in zip(
        soup.find_all("p", class_="CoinsListstyles__Code-sc-1c8245s-24 lgioIM"),
        soup.find_all("p", class_="CoinsListstyles__Name-sc-1c8245s-23 kVPjIs"),
        soup.find_all("td", class_="CoinsListstyles__Price-sc-1c8245s-25 fYNuHQ")):
    
    code = code_tag.get_text(strip=True)
    name = name_tag.get_text(strip=True)
    price_text = price_tag.get_text(strip=True)
    price = float(re.sub(r"[^\d.,]", "", price_text).replace(",", "."))
    coins.append((code, name, price))

# Sorting by price in descending order
coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

# Checking for headers existence in the file
header_needed = not os.path.isfile(csv_filename) or os.stat(csv_filename).st_size == 0

# Writing to CSV
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Writing headers only if the file is empty
    if header_needed:
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price ($)"])

    # Writing data
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([timestamp, index, coin[1], coin[0], coin[2]])

print(f"Saving data to '{csv_filename}'.")

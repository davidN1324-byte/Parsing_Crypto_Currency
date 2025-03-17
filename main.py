import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
from datetime import datetime

# File for saving history
csv_filename = "cryptocurrencies_history.csv"

# Read all User-Agents from the file
with open("user_agents.txt", "r") as file:
    user_agents = file.readlines()

# Select a random User-Agent
user_agent = random.choice(user_agents).strip()  # Take one line from the list and remove extra spaces and newline characters

# Request headers
headers = {
    "User-Agent": user_agent
}

url = "https://finance.ua/ua/crypto"
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

# Current date and time
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

coins = []
for code_tag, name_tag, price_tag in zip(
        soup.find_all("p", class_="CoinsListstyles__Code-sc-1c8245s-24 lgioIM"),
        soup.find_all("p", class_="CoinsListstyles__Name-sc-1c8245s-23 kVPjIs"),
        soup.find_all("td", class_="CoinsListstyles__Price-sc-1c8245s-25 fYNuHQ")):
    
    code = code_tag.get_text(strip=True)
    name = name_tag.get_text(strip=True)
    price_text = price_tag.get_text(strip=True)
    
    # Convert price to a number
    price = float(re.sub(r"[^\d.,]", "", price_text).replace(",", "."))
    coins.append((code, name, price))

# Sort in descending order by price
coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

# Check if the file exists and is not empty
file_exists = os.path.isfile(csv_filename) and os.path.getsize(csv_filename) > 0

# Open the file in append mode
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # If the file is being created for the first time, write the header
    if not file_exists:
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price  ($)"])

    # Write data with a timestamp
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([timestamp, index, coin[1], coin[0], coin[2]])

print(f"Data saved in '{csv_filename}' with history.")

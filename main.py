import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
from datetime import datetime

# File to store the history
csv_filename = "cryptocurrencies_history.csv"
max_records = 300  # Maximum number of records to store in the file

# Read all User-Agent strings from the file
with open("user_agents.txt", "r") as file:
    user_agents = file.readlines()

# Select a random User-Agent
user_agent = random.choice(user_agents).strip()  # Pick one string from the list and remove extra spaces and newlines

# Headers for the request
headers = {
    "User-Agent": user_agent
}

url = "https://finance.ua/ua/crypto"
response = requests.get(url, headers=headers)

# Parse the HTML response
soup = BeautifulSoup(response.text, "html.parser")

# Current timestamp
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

coins = []
# Extract coin data from the page
for code_tag, name_tag, price_tag in zip(
        soup.find_all("p", class_="CoinsListstyles__Code-sc-1c8245s-24 lgioIM"),
        soup.find_all("p", class_="CoinsListstyles__Name-sc-1c8245s-23 kVPjIs"),
        soup.find_all("td", class_="CoinsListstyles__Price-sc-1c8245s-25 fYNuHQ")):
    
    code = code_tag.get_text(strip=True)
    name = name_tag.get_text(strip=True)
    price_text = price_tag.get_text(strip=True)
    
    # Convert price to a float
    price = float(re.sub(r"[^\d.,]", "", price_text).replace(",", "."))
    coins.append((code, name, price))

# Sort coins by price in descending order
coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

# Check if the file exists and is not empty
file_exists = os.path.isfile(csv_filename) and os.path.getsize(csv_filename) > 0

# Read the current data from the file
existing_data = []
if file_exists:
    with open(csv_filename, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        existing_data = list(reader)

# Open the file in append mode to add new data
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # If the file is being created, write the header
    if not file_exists:
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price ($)"])

    # Write the new data with the timestamp
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([timestamp, index, coin[1], coin[0], coin[2]])

    # Keep only the last max_records rows
    all_data = existing_data + [(timestamp, index, coin[1], coin[0], coin[2]) for index, coin in enumerate(coins_sorted[:10], start=1)]
    if len(all_data) > max_records:
        all_data = all_data[-max_records:]

    # Rewrite the file with the limited number of records
    with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price ($)"])
        writer.writerows(all_data)

print(f"Data has been saved to '{csv_filename}' with history.")

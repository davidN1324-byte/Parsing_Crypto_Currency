import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
from datetime import datetime

# Файл для сохранения истории
csv_filename = "cryptocurrencies_history.csv"

# Читаем User-Agent'ы
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

# Сортируем по убыванию цены
coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

# Проверка на существование заголовков в файле
header_needed = not os.path.isfile(csv_filename) or os.stat(csv_filename).st_size == 0

# Запись в CSV
with open(csv_filename, mode="a", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)

    # Записываем заголовки только если файл пуст
    if header_needed:
        writer.writerow(["Date and Time", "#", "Full Name", "Abbreviation", "Price ($)"])

    # Записываем данные
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([timestamp, index, coin[1], coin[0], coin[2]])

print(f"Данные сохранены в '{csv_filename}'.")

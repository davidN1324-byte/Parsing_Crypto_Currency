import requests
from bs4 import BeautifulSoup
import re
import random
import csv
import os
from datetime import datetime

# Файл для сохранения истории
csv_filename = "cryptocurrencies_history.csv"

# Считываем все User-Agent из файла
with open("user_agents.txt", "r") as file:
    user_agents = file.readlines()

# Выбираем случайный User-Agent
user_agent = random.choice(user_agents).strip()  # Берем одну строку из списка и удаляем лишние пробелы и символы новой строки

# Заголовки для запроса
headers = {
    "User-Agent": user_agent
}

url = "https://finance.ua/ua/crypto"
response = requests.get(url, headers=headers)

soup = BeautifulSoup(response.text, "html.parser")

coins = []
for code_tag, name_tag, price_tag in zip(
        soup.find_all("p", class_="CoinsListstyles__Code-sc-1c8245s-24 lgioIM"),
        soup.find_all("p", class_="CoinsListstyles__Name-sc-1c8245s-23 kVPjIs"),
        soup.find_all("td", class_="CoinsListstyles__Price-sc-1c8245s-25 fYNuHQ")):
    
    code = code_tag.get_text(strip=True)
    name = name_tag.get_text(strip=True)
    price_text = price_tag.get_text(strip=True)
    
    # Преобразуем цену в число (удаляем символы '$' и пробелы)
    price = float(re.sub(r"[^\d.,]", "", price_text).replace(",", "."))  # Если разделители — запятые, заменяем их на точку
    coins.append((code, name, price))

# Сортируем валюты по цене (по убыванию)
coins_sorted = sorted(coins, key=lambda x: x[2], reverse=True)

# Записываем данные в CSV файл
with open("cryptocurrencies.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Записываем заголовок
    writer.writerow(["№", "Полное название", "Аббревиатура", "Цена ($)"])
    # Записываем данные
    for index, coin in enumerate(coins_sorted[:10], start=1):
        writer.writerow([index, coin[1], coin[0], coin[2]])

print("Данные успешно сохранены в файл 'cryptocurrencies.csv'")
import requests
from bs4 import BeautifulSoup
import re

url = "https://finance.ua/ua/crypto"
response = requests.get(url)

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
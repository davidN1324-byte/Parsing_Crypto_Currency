import requests
from bs4 import BeautifulSoup

url = "https://finance.ua/ua/crypto"
response = requests.get(url)

soup = BeautifulSoup(response.text, "html.parser")

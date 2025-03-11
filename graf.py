import pandas as pd
import matplotlib.pyplot as plt

# Читаем данные из CSV
df = pd.read_csv("cryptocurrencies_history.csv")

# Преобразуем столбец с датой в формат datetime
df['Date and Time'] = pd.to_datetime(df['Date and Time'])

# Группируем по дате и криптовалюте
df_grouped = df[['Date and Time', 'Abbreviation', 'Price ($)']].groupby(['Date and Time', 'Abbreviation']).last().reset_index()

# Строим график
plt.figure(figsize=(10, 6))

for coin in df_grouped['Abbreviation'].unique():
    coin_data = df_grouped[df_grouped['Abbreviation'] == coin]
    plt.plot(coin_data['Date and Time'], coin_data['Price ($)'], label=coin)

plt.title("Change of cryptocurrency prices")
plt.xlabel("Date and Time")
plt.ylabel("Price ($)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
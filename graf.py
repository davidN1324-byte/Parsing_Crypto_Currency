import pandas as pd
import matplotlib.pyplot as plt

# Читаем данные из CSV
df = pd.read_csv("cryptocurrencies_history.csv")

# Преобразуем столбец с датой в формат datetime
df['Дата и время'] = pd.to_datetime(df['Дата и время'])

# Группируем по дате и криптовалюте
df_grouped = df[['Дата и время', 'Аббревиатура', 'Цена ($)']].groupby(['Дата и время', 'Аббревиатура']).last().reset_index()

# Строим график
plt.figure(figsize=(10, 6))

for coin in df_grouped['Аббревиатура'].unique():
    coin_data = df_grouped[df_grouped['Аббревиатура'] == coin]
    plt.plot(coin_data['Дата и время'], coin_data['Цена ($)'], label=coin)

plt.title("Изменение цены криптовалют")
plt.xlabel("Дата и время")
plt.ylabel("Цена ($)")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()
plt.show()
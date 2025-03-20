import pandas as pd
import plotly.graph_objects as go
import os

# Reading data from CSV
df = pd.read_csv("cryptocurrencies_history.csv")

# We will convert the date column to the `datetime` format.
df['Date and Time'] = pd.to_datetime(df['Date and Time'])

# We group by date and cryptocurrency.
df_grouped = df[['Date and Time', 'Abbreviation', 'Price ($)']].groupby(['Date and Time', 'Abbreviation']).last().reset_index()

# We create an interactive chart.
fig = go.Figure()

# We add a line for each cryptocurrency.
for coin in df_grouped['Abbreviation'].unique():
    coin_data = df_grouped[df_grouped['Abbreviation'] == coin]
    fig.add_trace(go.Scatter(
        x=coin_data['Date and Time'],
        y=coin_data['Price ($)'],
        mode='lines',
        name=coin,
        hoverinfo='x+y+name',  # It displays information on hover.
        line=dict(width=2)
    ))

# Chart settings.
fig.update_layout(
    title="Cryptocurrency Price Changes",
    xaxis_title="Date and Time",
    yaxis_title="Price ($)",
    legend_title="Crypto",
    xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S'),
    hovermode="closest"  # Interactive mode.
)

# Save the chart as an HTML file
fig.write_html("docs/crypto_chart.html")
print("Chart saved in docs/crypto_chart.html")
import pandas as pd
import plotly.graph_objects as go

# Read data from CSV
df = pd.read_csv("cryptocurrencies_history.csv")

# Ensure that the first row is not a duplicated header
if df.iloc[0, 0] == "Date and Time":
    df = df.iloc[1:].reset_index(drop=True)

# Convert 'Date and Time' column to datetime format
df['Date and Time'] = pd.to_datetime(df['Date and Time'], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# Remove rows where 'Date and Time' could not be converted
df = df.dropna(subset=['Date and Time'])

# Group by date and cryptocurrency, keeping the last recorded price
df_grouped = df[['Date and Time', 'Abbreviation', 'Price ($)']].groupby(['Date and Time', 'Abbreviation']).last().reset_index()

# Sort by date in descending order (latest prices first)
df_grouped = df_grouped.sort_values(by="Date and Time", ascending=False)

# Create an interactive chart
fig = go.Figure()

# Add a line for each cryptocurrency
for coin in df_grouped['Abbreviation'].unique():
    coin_data = df_grouped[df_grouped['Abbreviation'] == coin]
    fig.add_trace(go.Scatter(
        x=coin_data['Date and Time'],
        y=coin_data['Price ($)'],
        mode='lines',
        name=coin,
        hoverinfo='x+y+name',
        line=dict(width=2)
    ))

# Configure chart settings
fig.update_layout(
    title="Cryptocurrency Price Changes",
    xaxis_title="Date and Time",
    yaxis_title="Price ($)",
    legend_title="Cryptocurrency",
    xaxis=dict(tickformat='%Y-%m-%d %H:%M:%S'),
    hovermode="closest"
)

# Save the chart as an HTML file
fig.write_html("docs/crypto_chart.html")
print("Chart saved in docs/crypto_chart.html")

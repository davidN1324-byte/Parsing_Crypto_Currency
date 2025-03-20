import pandas as pd
import plotly.graph_objects as go
import os

# Check for CSV file existence
csv_filename = "cryptocurrencies_history.csv"
if not os.path.exists(csv_filename):
    print(f"Файл {csv_filename} не найден. График не будет построен.")
    exit(1)

# Check for empty file
if os.stat(csv_filename).st_size == 0:
    print(f"Файл {csv_filename} пуст. Нет данных для графика.")
    exit(1)

# Read data from CSV
df = pd.read_csv(csv_filename)

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

# Configure chart settings (white background, grid, better readability)
fig.update_layout(
    title="Cryptocurrency Price Changes",
    xaxis_title="Date and Time",
    yaxis_title="Price ($)",
    legend_title="Cryptocurrency",
    xaxis=dict(
        tickformat='%Y-%m-%d %H:%M:%S',
        showgrid=True,
        gridcolor="rgba(200, 200, 200, 0.3)",  # Light gray grid
        tickangle=-45  # Better readability
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor="rgba(200, 200, 200, 0.3)"
    ),
    hovermode="closest",
    plot_bgcolor="white",  # Белый фон
    paper_bgcolor="white",
    font=dict(
        family="Roboto, sans-serif",
        size=14,
        color="black"
    ),
    margin=dict(l=40, r=40, t=50, b=50),  # Adequate spacing
    width=1200,
    height=600
)

# Save the chart as an HTML file
fig.write_html("docs/crypto_chart.html")
print("Chart saved in docs/crypto_chart.html")

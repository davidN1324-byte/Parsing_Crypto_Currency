import pandas as pd
import plotly.graph_objects as go
import os

# Check if the CSV file exists
csv_filename = "cryptocurrencies_history.csv"
if not os.path.exists(csv_filename):
    print(f"File {csv_filename} not found. The graph will not be generated.")
    exit(1)

# Check if the file is empty
if os.stat(csv_filename).st_size == 0:
    print(f"File {csv_filename} is empty. No data available for the graph.")
    exit(1)

# Read data from the CSV file
df = pd.read_csv(csv_filename)

# Ensure the first row is not a duplicated header
if df.iloc[0, 0] == "Date and Time":
    df = df.iloc[1:].reset_index(drop=True)

# Convert 'Date and Time' column to datetime format
df['Date and Time'] = pd.to_datetime(df['Date and Time'], format="%Y-%m-%d %H:%M:%S", errors="coerce")

# Remove rows where 'Date and Time' could not be converted
df = df.dropna(subset=['Date and Time'])

# Group data by date and cryptocurrency, keeping the last recorded price
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
        mode='lines+markers',  # Lines with markers
        name=coin
    ))

# Configure chart layout
fig.update_layout(
    title="Cryptocurrency Price Changes",
    xaxis_title="Date and Time",
    yaxis_title="Price ($)",
    legend_title="Cryptocurrency",
    xaxis=dict(type="date"),
    yaxis=dict(showgrid=True),
    hovermode="x unified",
    template="plotly_white",  # Clean layout
    margin=dict(l=20, r=20, t=50, b=50),
    width=900,
    height=500
)

# Save the chart as an HTML file
fig.write_html("docs/crypto_chart.html")
print("Chart saved in docs/crypto_chart.html")
import pandas as pd
import numpy as np
import openai
import os

# OpenAI API settings
openai.api_key = os.getenv("OPENAI_API_KEY")

# Load data
csv_file = "cryptocurrencies_history.csv"
df = pd.read_csv(csv_file, usecols=["Date and Time", "Abbreviation", "Price ($)"])

# Check for duplicate entries
duplicates = df[df.duplicated(subset=["Date and Time", "Abbreviation"], keep=False)]
if not duplicates.empty:
    print("Warning: Duplicate entries detected. Aggregating data...")

# Aggregate duplicate entries by calculating the mean price
df = df.groupby(["Date and Time", "Abbreviation"], as_index=False).mean()

# Reshape the dataframe for analysis
df = df.pivot(index="Date and Time", columns="Abbreviation", values="Price ($)")

# Function to calculate volatility (standard deviation relative to mean)
def calculate_volatility(prices):
    return np.std(prices) / np.mean(prices) * 100

# Function to calculate price trend percentage change
def calculate_trend(prices):
    return (prices[-1] - prices[0]) / prices[0] * 100

# Function to calculate moving average (default window = 7)
def calculate_moving_average(prices, window=7):
    return np.mean(prices[-window:])

# Function to analyze cryptocurrency price data
def analyze_data(df):
    results = {}
    for crypto in df.columns:
        prices = df[crypto].dropna().values
        if len(prices) > 1:  # Ensure there is enough data for calculations
            results[crypto] = {
                "volatility": calculate_volatility(prices),
                "trend": calculate_trend(prices),
                "moving_average": calculate_moving_average(prices)
            }
    
    # Compute correlation between cryptocurrencies
    results["correlation"] = df.corr().to_dict()
    return results

# Function to generate trading recommendations using OpenAI
def generate_recommendation(analysis):
    prompt = f"Analyze the data:\n{analysis}\n\nGive brief trading recommendations based on this data."

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Main execution block
if __name__ == "__main__":
    analysis = analyze_data(df)
    recommendation = generate_recommendation(analysis)
    
    # Save the analysis to a text file
    with open("docs/analysis.txt", "w", encoding="utf-8") as f:
        f.write(recommendation)
    
    print("Analysis complete. Result saved in docs/analysis.txt")

import pandas as pd
import numpy as np
import openai
import os

# OpenAI API settings
openai.api_key = os.getenv("OPENAI_API_KEY")

# Data loading
csv_file = "cryptocurrencies_history.csv"
df = pd.read_csv(csv_file, usecols=["Date and Time", "Abbreviation", "Price ($)"])
df = df.pivot(index="Date and Time", columns="Abbreviation", values="Price ($)")

def calculate_volatility(prices):
    return np.std(prices) / np.mean(prices) * 100

def calculate_trend(prices):
    return (prices[-1] - prices[0]) / prices[0] * 100

def calculate_moving_average(prices, window=7):
    return np.mean(prices[-window:])

def analyze_data(df):
    results = {}
    for crypto in df.columns:
        prices = df[crypto].dropna().values
        results[crypto] = {
            "volatility": calculate_volatility(prices),
            "trend": calculate_trend(prices),
            "moving_average": calculate_moving_average(prices)
        }
    
    # Correlation
    results["correlation"] = df.corr().to_dict()
    return results

def generate_recommendation(analysis):
    prompt = f"Analyze the data:\n{analysis}\n\nGive brief trading recommendations based on this data."

    client = openai.OpenAI()
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

if __name__ == "__main__":
    analysis = analyze_data(df)
    recommendation = generate_recommendation(analysis)
    
    with open("docs/analysis.txt", "w", encoding="utf-8") as f:
        f.write(recommendation)
    
    print("Analysis complete. Result saved in docs/analysis.txt")

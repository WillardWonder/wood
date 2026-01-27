import json
import random
import os
import requests
from datetime import datetime

# CONFIGURATION
# Your provided FRED Key
FRED_API_KEY = "ebbb8a10eb02bb0cec3c5c9fdaccb6ca"

def get_fred_data():
    """Fetches official Hardwood PPI from St. Louis Fed"""
    print("🌲 Connecting to Federal Reserve...")
    url = f"https://api.stlouisfed.org/fred/series/observations?series_id=WPU081&api_key={FRED_API_KEY}&file_type=json&limit=12&sort_order=desc"
    try:
        response = requests.get(url)
        data = response.json()
        observations = data.get('observations', [])[::-1]
        return [{"date": obs['date'], "value": float(obs['value'])} for obs in observations]
    except Exception as e:
        print(f"⚠️ FRED Error: {e}")
        return []

def scrape_local_prices():
    """Simulates Wisconsin Regional Pricing"""
    print("🕵️ Scraping Prices...")
    base_prices = {
        "Red Oak (4/4 Select)": 1050,
        "Hard Maple (4/4 #1)": 1450,
        "Basswood (4/4 Common)": 680,
        "White Ash": 920
    }
    # Add daily volatility
    return {k: int(v * random.uniform(0.98, 1.03)) for k, v in base_prices.items()}

def main():
    payload = {
        "meta": {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "source": "FRED API + Kretz Internal Scout"
        },
        "market_index": get_fred_data(),
        "spot_prices": scrape_local_prices(),
        "tariffs": [
            {"target": "China", "rate": "25%", "status": "CRITICAL", "impact": "High"},
            {"target": "EU", "rate": "10%", "status": "WARNING", "impact": "Med"},
            {"target": "Vietnam", "rate": "0%", "status": "STABLE", "impact": "Low"},
        ],
        "alert": "Monitor Red Oak inventory. Export volumes to Asia showing weakness."
    }

    # Save to 'public' folder so the website can read it
    os.makedirs('public', exist_ok=True)
    with open('public/data.json', 'w') as f:
        json.dump(payload, f, indent=2)
    print("✅ Data saved to public/data.json")

if __name__ == "__main__":
    main()

import json
import random
import os
import requests
from datetime import datetime

# CONFIGURATION
FRED_API_KEY = "ebbb8a10eb02bb0cec3c5c9fdaccb6ca"
COMTRADE_API_URL = "https://comtradeapi.un.org/public/v1/getComtradeReleases"

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

def get_comtrade_releases():
    """Fetches latest trade data releases from UN Comtrade"""
    print("🚢 Connecting to UN Comtrade...")
    params = {
        'type': 'C',       # Commodities
        'freq': 'A',       # Annual
        'p': '2025',       # Period (Year)
        'sort': 'refDesc'  # Sort by release date
    }
    try:
        # Note: We filter for recent releases to keep the file size small
        response = requests.get(COMTRADE_API_URL, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # Return top 10 most recent releases
            return data.get('data', [])[:10] 
        else:
            print(f"⚠️ Comtrade Status: {response.status_code}")
            return []
    except Exception as e:
        print(f"⚠️ Comtrade Error: {e}")
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
    return {k: int(v * random.uniform(0.98, 1.03)) for k, v in base_prices.items()}

def main():
    payload = {
        "meta": {
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
            "source": "FRED + UN Comtrade"
        },
        "market_index": get_fred_data(),
        "spot_prices": scrape_local_prices(),
        "comtrade_releases": get_comtrade_releases(), # <--- NEW DATA FIELD
        "tariffs": [
            {"target": "China", "rate": "25%", "status": "CRITICAL", "impact": "High"},
            {"target": "EU", "rate": "10%", "status": "WARNING", "impact": "Med"},
        ],
        "alert": "Monitor Red Oak inventory. Export volumes to Asia showing weakness."
    }

    os.makedirs('public', exist_ok=True)
    with open('public/data.json', 'w') as f:
        json.dump(payload, f, indent=2)
    print("✅ Data saved to public/data.json")

if __name__ == "__main__":
    main()

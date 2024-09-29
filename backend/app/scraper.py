import requests

def scrape_fighter_data(api_url: str):
    response = requests.get(api_url)
    data = response.json()
    # Process and return relevant data
    return data

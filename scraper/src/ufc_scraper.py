import requests
from bs4 import BeautifulSoup

def scrape_ufc():
    url = 'https://www.ufc.com/events'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract fight data here
    # Save results in a structured format (e.g., JSON or direct to SQLite)

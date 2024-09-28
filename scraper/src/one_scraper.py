import requests
from bs4 import BeautifulSoup

# TODO
def scrape_ofc():
    url = ''
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract fight data here
    # Save results in a structured format (e.g., JSON or direct to SQLite)

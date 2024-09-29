from abc import ABC, abstractmethod
import requests
from bs4 import BeautifulSoup
import psycopg2
import time
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("DATABASE_USER")
DB_PW = os.getenv("DATABASE_PW")
DB_HOST = os.getenv("DATABASE_HOST")
DB_PORT = os.getenv("DATABASE_PORT")
DB_NAME = os.getenv("DATABASE_NAME")

class MMA_Scraper(ABC):
    name = "MMA Scraper"
    
    def __init__(self):
        pass

    # Abstract method for scraping
    @abstractmethod
    def scrape(self) -> None:
        pass
    
    
class UFC_Scraper(MMA_Scraper):
    name = "UFC Scraper"
    
    def __init__(self, db_config: Dict[str, Any]):
        super().__init__()
        self.base_url = "http://ufcstats.com/statistics/events/completed?page="
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def scrape(self) -> None:
        page_number = 1
        has_more_pages = True

        while has_more_pages:
            soup = self.get_page_html(page_number)
            event_list = soup.find_all("a", class_="b-link b-link_style_black")
            
            if not event_list:
                has_more_pages = False  # Exit if no more events are found on the page
            else:
                for event in event_list:
                    event_name = event.text.strip()
                    event_url = event['href']
                    self.scrape_fights(event_url, event_name)  # Scrape fights and insert into DB

                page_number += 1  # Move to the next page
                time.sleep(1)  # Delay to avoid overloading the server

        # Commit changes and close the database connection
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_page_html(self, page_number: int) -> BeautifulSoup:
        url = self.base_url + str(page_number)
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    def scrape_fights(self, event_url: str, event_name: str) -> None:
        event_response = requests.get(event_url)
        event_soup = BeautifulSoup(event_response.content, "html.parser")
        fight_table = event_soup.find("tbody")

        if fight_table:
            for fight_row in fight_table.find_all("tr"):
                fight_data = fight_row.find_all("td")
                
                if len(fight_data) >= 7:
                    fighter_1 = fight_data[1].find_all("p")[0].text.strip()  # First fighter name
                    fighter_2 = fight_data[1].find_all("p")[1].text.strip()  # Second fighter name
                    result = fight_data[0].text.strip()  # Win/Loss
                    method = fight_data[7].text.strip()  # Method of victory
                    
                    # Insert fighters into the fighters table
                    self.insert_fighter(fighter_1)
                    self.insert_fighter(fighter_2)
                    
                    # Insert fight details into the fights table
                    self.insert_fight(fighter_1, fighter_2, result, method)
        
        time.sleep(1)  # Delay between fights scrapes

    def insert_fighter(self, fighter_name: str) -> None:
        self.cursor.execute("""
            INSERT INTO fighters (name, elo_rating)
            VALUES (%s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (fighter_name, self.init_elo(fighter_name)))

    def insert_fight(self, fighter_1: str, fighter_2: str, result: str, method: str) -> None:
        self.cursor.execute("""
            INSERT INTO fights (fighter_1, fighter_2, result, method)
            VALUES (%s, %s, %s, %s)
        """, (fighter_1, fighter_2, result, method))

    def init_elo(self, fighter_name: str) -> float:
        # Placeholder function for ELO rating calculation
        # Implement your ELO calculation logic here
        return 1000.0  # Default ELO rating
    
class ONE_Scraper(MMA_Scraper):
    name = "ONE Scraper"
    
    def __init__(self, db_config: Dict[str, Any]):
        super().__init__()
        self.base_url = ""
        self.connection = psycopg2.connect(**db_config)
        self.cursor = self.connection.cursor()

    def scrape(self) -> None:
        page_number = 1
        has_more_pages = True

        while has_more_pages:
            soup = self.get_page_html(page_number)
            event_list = soup.find_all("a", class_="b-link b-link_style_black")
            
            if not event_list:
                has_more_pages = False  # Exit if no more events are found on the page
            else:
                for event in event_list:
                    event_name = event.text.strip()
                    event_url = event['href']
                    self.scrape_fights(event_url, event_name)  # Scrape fights and insert into DB

                page_number += 1  # Move to the next page
                time.sleep(1)  # Delay to avoid overloading the server

        # Commit changes and close the database connection
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

    def get_page_html(self, page_number: int) -> BeautifulSoup:
        url = self.base_url + str(page_number)
        response = requests.get(url)
        return BeautifulSoup(response.content, "html.parser")

    def scrape_fights(self, event_url: str, event_name: str) -> None:
        event_response = requests.get(event_url)
        event_soup = BeautifulSoup(event_response.content, "html.parser")
        fight_table = event_soup.find("tbody")

        if fight_table:
            for fight_row in fight_table.find_all("tr"):
                fight_data = fight_row.find_all("td")
                
                if len(fight_data) >= 7:
                    fighter_1 = fight_data[1].find_all("p")[0].text.strip()  # First fighter name
                    fighter_2 = fight_data[1].find_all("p")[1].text.strip()  # Second fighter name
                    result = fight_data[0].text.strip()  # Win/Loss
                    method = fight_data[7].text.strip()  # Method of victory
                    
                    # Insert fighters into the fighters table
                    self.insert_fighter(fighter_1)
                    self.insert_fighter(fighter_2)
                    
                    # Insert fight details into the fights table
                    self.insert_fight(fighter_1, fighter_2, result, method)
        
        time.sleep(1)  # Delay between fights scrapes

    def insert_fighter(self, fighter_name: str) -> None:
        self.cursor.execute("""
            INSERT INTO fighters (name, elo_rating)
            VALUES (%s, %s)
            ON CONFLICT (name) DO NOTHING
        """, (fighter_name, self.init_elo(fighter_name)))

    def insert_fight(self, fighter_1: str, fighter_2: str, result: str, method: str) -> None:
        self.cursor.execute("""
            INSERT INTO fights (fighter_1, fighter_2, result, method)
            VALUES (%s, %s, %s, %s)
        """, (fighter_1, fighter_2, result, method))

    def init_elo(self, fighter_name: str) -> float:
        # Placeholder function for ELO rating calculation
        # Implement your ELO calculation logic here
        return 1000.0  # Default ELO rating
    


if __name__ == "__main__":
    db_config = {
        'dbname': DB_NAME,
        'user': DB_USER,
        'password': DB_PW,
        'host': DB_HOST,
        'port': DB_PORT
    }
    
    ufc_scraper_instance = UFC_Scraper(db_config)
    ufc_scraper_instance.scrape()
    print("Scraping completed and data inserted into the database.")

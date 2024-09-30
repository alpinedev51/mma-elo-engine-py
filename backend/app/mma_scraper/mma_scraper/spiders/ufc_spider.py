import scrapy
from items import FightItem

class UFCSpider(scrapy.Spider):
    name = "ufc"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
    
    def parse(self, response):
        # Loop directly over the elements that contain the event names and links
        for event in response.css("a.b-link.b-link_style_black"):
            event_name = event.css("::text").get().strip(),
            event_link = event.attrib["href"]
            
            # Make a request to scrape fight details using the event link
            yield scrapy.Request(
                url=event_link, 
                callback=self.parse_fights, 
                meta={'event_name': event_name}
            )
    
    def parse_fights(self, response):
        event_name = response.meta['event_name']
        fight_table = response.css("tbody")

        if fight_table:
            for fight_row in fight_table.css("tr"):
                fight_data = fight_row.css("td")
                
                if len(fight_data) >= 8:
                    fighter_1 = fight_data[1].css("p:nth-child(1)::text").get().strip()  # First fighter name
                    fighter_2 = fight_data[1].css("p:nth-child(2)::text").get().strip()  # Second fighter name
                    result = fight_data[0].css("::text").get().strip()  # Win/Loss
                    method = fight_data[7].css("::text").get().strip()  # Method of victory

                    # Yield a Scrapy item to be processed by the pipeline
                    fight_item = FightItem(
                        event_name=event_name,
                        fighter_1=fighter_1,
                        fighter_2=fighter_2,
                        result=result,
                        method=method
                    )
                    
                    yield fight_item
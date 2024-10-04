import scrapy
from mma_scraper.items import FightInfoItem

class UFCSpider(scrapy.Spider):
    name = "ufc_spider"
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
            
        url_to_all = response.css('a.b-statistics__paginate-link[href*="?page=all"]::attr(href)').get()
        yield scrapy.Request(
            url=url_to_all,
            callback=self.parse
        )
    
    def parse_fights(self, response):
        event_name = response.meta['event_name']
        fight_table = response.css("tbody")

        if fight_table:
            for fight_row in fight_table.css("tr"):
                fight_data = fight_row.css("td")
                if len(fight_data) >= 8:
                    fighter_1 = fight_data[1].css("p:nth-of-type(1) a::text").get().strip()  # First fighter name
                    fighter_2 = fight_data[1].css("p:nth-of-type(2) a::text").get().strip()  # Second fighter name
                    result = fight_data[0].css("a.b-flag .b-flag__text::text").get().strip()  # Win/Loss
                    method = fight_data[7].css("p:nth-of-type(1)::text").get().strip()  # Method of victory

                    # Yield a Scrapy item to be processed by the pipeline
                    fight_info_item = FightInfoItem(
                        event_name_info=event_name,
                        fighter_1_name_info=fighter_1,
                        fighter_2_name_info=fighter_2,
                        result_info=result,
                        method_info=method
                    )
                    
                    yield fight_info_item
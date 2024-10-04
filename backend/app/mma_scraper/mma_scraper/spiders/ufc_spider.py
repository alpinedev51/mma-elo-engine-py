import scrapy
from mma_scraper.items import FightInfoItem
from datetime import datetime

class UFCSpider(scrapy.Spider):
    name = "ufc_spider"
    allowed_domains = ["ufcstats.com"]
    start_urls = ["http://ufcstats.com/statistics/events/completed?page=all"]
    
    def parse(self, response):
        # get all dates of the page that follow a valid event
        date_strings = response.xpath('//a[@class="b-link b-link_style_black"]/following-sibling::span[@class="b-statistics__date"]/text()').getall()
        # Loop directly over the elements that contain the event names and links
        for idx, event in enumerate(response.css("a.b-link.b-link_style_black")):
            event_name = event.css("::text").get().strip(),
            event_link = event.attrib["href"]
            # use XPath instead to target the span only when the a tag above it has the correct class
            date_string = date_strings[idx].strip()
            event_date = datetime.strptime(date_string, "%B %d, %Y").date()
            
            # Make a request to scrape fight details using the event link
            yield scrapy.Request(
                url=event_link, 
                callback=self.parse_fights, 
                meta={"event_name": event_name, "event_date": event_date}
            )
            
        #url_to_all = response.css('a.b-statistics__paginate-link[href*="?page=all"]::attr(href)').get()
        #yield scrapy.Request(
        #    url=url_to_all,
        #    callback=self.parse
        #)
    
    def parse_fights(self, response):
        event_name = response.meta["event_name"]
        event_date = response.meta["event_date"]
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
                        method_info=method,
                        event_date_info=event_date
                    )
                    
                    yield fight_info_item
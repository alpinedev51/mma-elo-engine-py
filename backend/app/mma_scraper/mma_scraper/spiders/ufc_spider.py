import scrapy

class UFCSpider(scrapy.Spider):
    name = "ufc"
    start_urls = ["http://ufcstats.com/statistics/events/completed"]
    
    def parse(self, response):
        # Loop directly over the elements that contain the event names and links
        for event in response.css("a.b-link.b-link_style_black"):
            yield {
                "name": event.css("::text").get().strip(),
                "link": event.attrib["href"]
            }
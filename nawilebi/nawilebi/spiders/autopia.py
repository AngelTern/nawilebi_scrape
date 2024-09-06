import scrapy


class AutopiaSpider(scrapy.Spider):
    name = "autopia"
    allowed_domains = ["autopia.ge"]
    start_urls = ["https://autopia.ge"]

    def parse(self, response):
        pass

import scrapy


class TopautopartsSpider(scrapy.Spider):
    name = "topautoparts"
    allowed_domains = ["topautoparts.ge"]
    start_urls = ["https://topautoparts.ge/"]

    def parse(self, response):
        pass

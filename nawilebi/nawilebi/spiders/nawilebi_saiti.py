import scrapy


class NawilebiSaitiSpider(scrapy.Spider):
    name = "nawilebi_saiti"
    allowed_domains = ["nawilebi.ge"]
    start_urls = ["https://nawilebi.ge/ka/parts"]
    start_page = 1
    def parse(self, response):
        
            
    def parse_model_page(self, response):
        pass

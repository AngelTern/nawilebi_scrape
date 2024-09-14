import scrapy


class PartscornerSpider(scrapy.Spider):
    name = "partscorner"
    allowed_domains = ["partscorner.ge"]
    start_urls = ["https://partscorner.ge/"]

    def parse(self, response):
        car_mark_list = response.css("body > section > div > div > div > div:nth-child(3) > div > div > div > div > div > section:nth-child(3) > div > div > div, body > section > div > div > div > div:nth-child(3) > div > div > div > div > div > section:nth-child(4) > div > div > div,body > section > div > div > div > div:nth-child(3) > div > div > div > div > div > section:nth-child(5) > div > div > div")
        
        for car_mark in car_mark_list:
            relative_url = car_mark.css("div > div > div > div > div > div.shop-img > a::attr(href)").get()
            yield response.follow("https://partscorner.ge/" + relative_url, callback = self.part_mark_page)

    def part_mark_page(self, response):
        pass
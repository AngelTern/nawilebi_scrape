import scrapy


class NawilebiSaitiSpider(scrapy.Spider):
    name = "nawilebi_saiti"
    allowed_domains = ["nawilebi.ge"]
    start_urls = ["https://nawilebi.ge/ka"]

    def parse(self, response):
        car_mark_list = response.css("#page-container > div.container.m-b-20 > div > section > div > div")
        
        for car_mark in car_mark_list:
            relative_url = car_mark.css("div a::attr(href)").get()
            car_mark_name = car_mark.css("div a::attr(title)").get().upper()
            
            yield response.follow(self.start_urls[0] + relative_url, callback = self.parse_model_page,
                                  meta = {"car_mark": car_mark_name})
            
    def parse_model_page(self, response):
        pass

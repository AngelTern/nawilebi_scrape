import scrapy


class AutopiaSpider(scrapy.Spider):
    name = "autopia"
    allowed_domains = ["autopia.ge"]
    start_urls = ["https://autopia.ge"]

    def parse(self, response):
        
        car_marks = response.css("div.car_marks").get()
        
        for car_mark in car_marks:
            relative_url = response.css("a ::attr(href)").get()
            car_mark_url = "https://autopia.ge" + relative_url
            
            yield response.follow(car_mark_url, callback=self.parse_case_page)
            
    
    def parse_car_mark(self, response):
        pass
    
    def parse_car_part(self, response):
        pass
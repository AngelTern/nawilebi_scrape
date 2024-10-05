import scrapy
from nawilebi.items import NawilebiItem

class SoloautoSpider(scrapy.Spider):
    name = "soloauto"
    allowed_domains = ["soloauto.ge"]
    start_urls = ["https://soloauto.ge/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "nawilebi.pipelines.NawilebiPipeline": 300,
            "nawilebi.pipelines.SoloautoPipeline": 200,
            #"nawilebi.pipelines.YearProcessPipeline": 300,
            "nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        #'DOWNLOAD_DELAY': 3,
    }
    
    
    def parse(self, response):
       car_mark_list = a = response.css("#content > div.page-content > div > section > div > div> div > div > div")
       
       for car_mark in car_mark_list:
           car_mark_url = car_mark.css("a::attr(href)").get()
           
           if car_mark_url:
               
               yield response.follow(car_mark_url, callback = self.parse_mark_page)
               
    def parse_mark_page(self, response):
        car_model_list = response.css("#content > div.page-content > div > section > div > div > div > div > div > div > ul li")
        
        for car_model in car_model_list:
            part_list_url = car_model.css("a::attr(href)").get()
            
            if part_list_url:
                
                yield response.follow(part_list_url, callback = self.parse_part_list)
                
    def parse_part_list(self, response):
        part_list = response.css("body > div.elementor > section > div > div > div > div > div > div > ul li")
        
        for part in part_list:
            part_url = part.css("a:nth-of-type(1)::attr(href)").get()
            
            if part_url:
                
                yield response.follow(part_url, callback = self.parse_part_page)
                
    def parse_part_page(self, response):
        item = NawilebiItem()
        
        item["car_mark"] = response.css("body > div > section > div > div > div > div > div > nav > a:nth-child(2)::text").get().strip()
        item["car_model"] = response.css("body > div > section > div > div > div > div > div > nav > a:nth-child(3)::text").get().strip()
        item["part_url"] = response.url
        item["website"] = "https://soloauto.ge/"
        item["part_full_name"] = response.css("div > section > div > div > div > section > div > div > div > div > div > div > div > h4::text").get().strip()
        item["price"] = response.css("div > section > div > div > div > section > div > div > div > div > div > div > div > p > span > bdi::text").get().strip()
        item["in_stock"] = True if response.css(".elementor-add-to-cart p::text").get().strip()  == "მარაგში" else False
        item["year"] = None
        item["start_year"] = None
        item["end_year"] = None
        
        yield item
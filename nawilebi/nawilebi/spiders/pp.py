import scrapy
from nawilebi.items import NawilebiItem

class PpSpider(scrapy.Spider):
    name = "pp"
    allowed_domains = ["pp.ge"]
    start_urls = ["https://pp.ge/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            #"nawilebi.pipelines.NawilebiPipeline": 100,
            #"nawilebi.pipelines.PpPipeline": 200,
            #"nawilebi.pipelines.YearProcessPipeline": 300,
            #"nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }
    
    
    def parse(self, response):
        car_mark_list= response.css("body > section.market-and-fullSearch > div.car_brands > div > div a")
        
        for car_mark in car_mark_list:
            car_mark_url = car_mark.css("::attr(href)").get()
            car_mark_name = car_mark.css("div h2::text").get()
            
            yield response.follow(car_mark_url, callback = self.parse_mark_page,
                                  meta= {"car_mark": car_mark_name})
            
    def parse_mark_page(self, response):
        part_list = response.css("#car-par > div > div > div > div.card-wrapper-view > div")
        
        for part in part_list:
            item = NawilebiItem()
            car_mark = response.meta["car_mark"]
            part_url = part.css("div a::attr(href)").get()
            
            part_full_name = part.css("div > a img::attr(alt)").get()
            car_model = part.css("div div.card_bottom div.card-brand-model::text").get()
            price = part.css("div div.card_bottom div.card_price div.card_price_amount::attr(data-price)").get()
            original_price = part.css("div div.card_bottom div.card_price div.card_price_amount::attr(data-old-price)").get()
            in_stock = part.css("div div.card_bottom div.card_price span p::text").get()
            '''in_stock_int = int(in_stock)
            item["in_stock"] =True if in_stock_int != 0 else False'''

            yield response.follow(part_url, callback = self.parse_part_page,
                                  meta =  {"car_mark": car_mark, "part_url": part_url, "part_full_name": part_full_name,
                                           "car_model": car_model, "price": price, "original_price": original_price, "in_stock": in_stock})
            
            
        navigation_list =response.css("#car-par > div > div > div > div.row.clearfix > div > nav > nav > ul li")
        
        if navigation_list:
            for nav in navigation_list:
                
                next_page_url = nav.css("span::attr(href)").get()
                if next_page_url and nav.css("a::attr(rel)").get() != "next":
                    yield response.follow(next_page_url, callback = self.parse_next_page,
                                          meta = {"car_mark": response.meta["car_mark"]})
                    
                    
    def parse_next_page(self, response):
        part_list = response.css("#car-par > div > div > div > div.card-wrapper-view > div")
        
        for part in part_list:
            item = NawilebiItem()
            car_mark = response.meta["car_mark"]
            part_url = part.css("div > a img::attr(href)").get()
            
            part_full_name = part.css("div a img::attr(alt)").get()
            car_model = part.css("div div.card_bottom div.card-brand-model::text").get()
            price = part.css("div div.card_bottom div.card_price div.card_price_amount::attr(data-price)").get()
            original_price = part.css("div div.card_bottom div.card_price div.card_price_amount::attr(data-old-price)").get()
            in_stock = part.css("div div.card_bottom div.card_price span p::text").get()
            '''in_stock_int = int(in_stock)
            item["in_stock"] =True if in_stock_int != 0 else False'''

            yield response.follow(part_url, callback = self.parse_part_page,
                                  meta =  {"car_mark": car_mark, "part_url": part_url, "part_full_name": part_full_name,
                                           "car_model": car_model, "price": price, "original_price": original_price, "in_stock": in_stock})
            
    def parse_part_page(self, response):
        item = NawilebiItem()
        
        item["year"] = response.css("#car-parts-wrapper-view > div > div.product_right > div.prod_main_info > div:nth-child(5) span:nth-of-type(1)::text").getall()
        item["city"] = response.css("#car-parts-wrapper-view > div > div.product_right > div.prod_main_info > div:nth-child(5) > span.prod_main_info_different > h4::text").get()
        item["car_mark"] = response.meta["car_mark"]
        item["part_url"] = response.meta["part_url"]
        item["part_full_name"] = response.meta["part_full_name"]
        item["car_model"] = response.meta["car_model"]
        item["price"] = response.meta["price"]
        item["original_price"] = response.meta["original_price"]
        item["in_stock"] = response.meta["in_stock"]
        item["website"] = "https://pp.ge/"
        
        
        
        yield item
                    

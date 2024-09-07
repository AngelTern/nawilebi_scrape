import scrapy
from nawilebi.items import NawilebiItem

class AutopiaSpider(scrapy.Spider):
    name = "autopia"
    allowed_domains = ["autopia.ge"]
    start_urls = ["https://autopia.ge"]

    def parse(self, response):
        
        start_url = response.url
        car_marks = response.css("div.car_marks").get()
        
        for car_mark in car_marks:
            relative_url = car_mark.css("a ::attr(href)").get()
            car_mark_url = "https://autopia.ge" + relative_url
            
            yield response.follow(car_mark_url, callback=self.parse_car_mark,
                                  meta = {"start_url": start_url})
            
    
    def parse_car_mark(self, response):
        
        start_url = response.meta["start_url"]
        products_list = response.css("div.products-list").get()
        
        for product in products_list:
            
            if "_product" not in product.css("div::attr(class)").get():
                pass
            else:
                car_url_relative = product.css("div.product-item-container div.right-block div.button-group a::attr(href)").get()
                car_url_full = "https://autopia.ge" + car_url_relative
                yield response.follow(car_url_full, callback = self.parse_car_part_list,
                                  meta = {"start_url": start_url})
            
    
    def parse_car_part_list(self, response):
        
        start_url = response.meta["start_url"]
        product_list_part = response.css("div.products-list").get()
        
        for product_part in product_list_part:
            
            if "_product" not in product_part.css("div::attr(class)").get():
                pass
            else:
                car_part_url_relative = product_part.css("div.left-block div.product-image-container a::attr(href)").get()
                car_part_url_full = "https://autopia.ge" + car_part_url_relative
                yield response.follow(car_part_url_full, callback = self.parse_car_part_page,
                                  meta = {"start_url": start_url})
                
    def parse_car_part_page(self, response):
        
        main_content = response.css("div.content-product-right > div")
        product_description = main_content[3].css(".inner-box-desc")
        
        NawilebiItem["website"] = response.meta["start_url"]
        NawilebiItem["part_url"] = response.url
        NawilebiItem["car_mark"] = product_description.css(".price-tax::text").get()
        NawilebiItem["part_full_name"] = main_content[0].css("h1::text").get()
        NawilebiItem["year"] = product_description.css("div:nth-of-type(3)::text").get()
        #NawilebiItem["oem"] = product_description.css("div.reward:nth-of-type(2) span::text").get()
        NawilebiItem["price"] = main_content[2].css("div.product_page_price span::text").get()
        NawilebiItem["in_stock"] = main_content[2].css("div:nth-of-type(2)::attr(class)").get()
        
        yield NawilebiItem
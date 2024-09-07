import scrapy
from nawilebi.items import NawilebiItem

class AutopiaSpider(scrapy.Spider):
    name = "autopia"
    allowed_domains = ["autopia.ge"]
    start_urls = ["https://autopia.ge"]

    def parse(self, response):
        
        start_url = response.url
        car_marks = response.css("div.car_marks > div")
        
        for car_mark in car_marks:
            relative_url = car_mark.css("a ::attr(href)").get()
            car_mark_url = "https://autopia.ge" + relative_url
            
            yield response.follow(car_mark_url, callback=self.parse_car_mark,
                                  meta = {"start_url": start_url})
            
    
    def parse_car_mark(self, response):
        start_url = response.meta["start_url"]

        # Ensure that products_list is a list of selector objects
        products_list = response.css("div.products-list > div")  # Select the direct div children

        for product in products_list:
            product_class = product.css("div::attr(class)").get()
            if product_class and "_product" not in product_class:
                pass
            else:
                car_url_relative = product.css("div.product-item-container div.right-block div.button-group a::attr(href)").get()
                car_url_full = "https://autopia.ge" + car_url_relative
                yield response.follow(car_url_full, callback=self.parse_car_part_list,
                                    meta={"start_url": start_url})

            
    
    def parse_car_part_list(self, response):
        start_url = response.meta["start_url"]
        
        # Ensure product_list_part is a list of selector objects
        product_list_part = response.css("div.products-list > div")  # Adjust the CSS selector if needed

        for product_part in product_list_part:
            # Extract the class attribute safely
            product_class = product_part.css("div::attr(class)").get()
            
            if product_class and "_product" not in product_class:
                pass
            else:
                car_part_url_relative = product_part.css("div.left-block div.product-image-container a::attr(href)").get()
                car_part_url_full = "https://autopia.ge" + car_part_url_relative
                yield response.follow(car_part_url_full, callback=self.parse_car_part_page,
                                    meta={"start_url": start_url})

                
    def parse_car_part_page(self, response):
        
        main_content = response.css("div.content-product-right > div")
        product_description = main_content[3].css(".inner-box-desc")
        item = NawilebiItem()
        
        
        item["website"] = response.meta["start_url"]
        item["part_url"] = response.url
        item["car_mark"] = response.css(".price-tax::text").get()
        item["part_full_name"] = response.css("div.content-product-right > div:nth-of-type(1) h1::text").get()
        item["year"] = response.css("div.inner-box-desc div:nth-of-type(3)::text").get()
        item["price"] = response.css("div.content-product-right > div:nth-of-type(3) span::text").get()
        
        if response.css("div.content-product-right > div:nth-of-type(3) div:nth-of-type(2)::attr(class)").get() == "modal-wrapper":
            item["in_stock"] = "in_stock"
        else:
            item["in_stock"] = "not_stock"
        #item["in_stock"] = response.css("div.content-product-right > div:nth-of-type(3) div:nth-of-type(2)::attr(class)").get()

        yield item
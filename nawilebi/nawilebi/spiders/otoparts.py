import scrapy
from nawilebi.items import NawilebiItem


class OtopartsSpider(scrapy.Spider):
    name = "otoparts"
    allowed_domains = ["otoparts.ge"]
    start_urls = ["https://otoparts.ge/dzaris-natsilebi/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            "nawilebi.pipelines.NawilebiPipeline": 100,
            "nawilebi.pipelines.CarpartsPipeline": 200,
            #"nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }
    
    

    def parse(self, response):
        sections_list = response.css("div.elementor-177 > section")
        
        for section in sections_list:
            car_marks_list = section.css("div.elementor-container > div")
            
            for car_mark in car_marks_list:
                car_model_url = car_mark.css("div div div a::attr(href)").get()
                car_mark_name = car_mark.css("div div div a img::attr(title)").get()
                
                yield response.follow(car_model_url, callback = self.parse_car_model,
                                      meta = {"car_mark": car_mark_name})
                
    def parse_car_model(self, response):
        car_models_sections = response.css("body > div.elementor.elementor-1130 > section.elementor-section.elementor-top-section.elementor-element.elementor-element-031c4e8.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div section")
        
        for section in car_models_sections:
            car_models_list = section.css("div > div")
            
            for car_model in car_models_list:
                car_model_url = car_model.css("div > div > div > div > div h1 a::attr(href)").get()
                yield response.follow(car_model_url, callback = self.parse_parts_list,
                                      meta = {"car_mark": response.meta["car_mark"]})
                
    def parse_parts_list(self, response):
        item = NawilebiItem()
        car_parts_list = response.css("body > div.elementor.elementor-19962.elementor-location-archive.product > section.elementor-section.elementor-top-section.elementor-element.elementor-element-664c33e8.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div > div > div > ul > li")
        
        for car_part in car_parts_list:
            item["website"] = "https://otoparts.ge/dzaris-natsilebi/"
            item["part_url"] = car_part.css("div .premium-woo-products-details-wrap a::attr(href)").get()
            item["part_full_name"] = car_part.css("div .premium-woo-products-details-wrap a h2::text").get()
            item["car_model"] = car_part.css("div .premium-woo-products-details-wrap span::text").get()
            item["price"] = car_part.css("div .premium-woo-products-details-wrap .premium-woo-product-info span span bdi::text").get()
            item["car_mark"] = response.meta["car_mark"]
            if car_part.css("div premium-woo-product-thumbnail span").get():
                item["in_stock"] = False
            else:
                item["in_stock"] = True
                

            

            

        
        
        
        
        
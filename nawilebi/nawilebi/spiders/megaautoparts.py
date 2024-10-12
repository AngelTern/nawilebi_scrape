import scrapy
from nawilebi.items import NawilebiItem
from utilities.additional_functions import adjust_car_name_for_url_megaauto

class MegaautopartsSpider(scrapy.Spider):
    name = "megaautoparts"
    allowed_domains = ["megaautoparts.ge"]
    start_urls = ["https://megaautoparts.ge/"]
    custom_settings = {
    'ITEM_PIPELINES': {
        "nawilebi.pipelines.NawilebiPipeline": 300,
        "nawilebi.pipelines.OtopartsPipeline": 200,
        "nawilebi.pipelines.SaveToMySQLPipeline": 900
    },
    'DOWNLOAD_DELAY': 0.5
    }

    def parse(self, response):
        car_mark_urls = response.css("#main > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div > div > div > div div div.jet-woo-categories-content div h5 a::attr(href)")
        
        
        '''car_mark_list = response.css("#main > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div > div > div > div")
        
        for car_mark in car_mark_list:
            car_model_page_url = car_mark.css("div div.jet-woo-categories-content div h5 a::attr(href)").get()
            car_mark_name = car_mark.css("div div.jet-woo-categories-content div h5 a::text").get()'''
            
        for car_mark_url in car_mark_urls:
            
            yield response.follow(car_mark_url, callback = self.parse_model_page,
                                  )
            
    def parse_model_page(self, response):
        car_model_urls = response.css("#main > div > div > section > div > div > div > div.elementor-element.elementor-widget.elementor-widget-jet-woo-categories > div > div > div > div div div.jet-woo-categories-content div h5 a::attr(href)")
        car_models = response.css(".jet-woo-categories-content .jet-woo-categories-title__wrap h5 a::text").getall()
        '''car_model_list = response.css("#main > div > div > section > div > div > div > div.elementor-element.elementor-widget.elementor-widget-jet-woo-categories > div > div > div > div")

        for car_model in car_model_list:
            car_parts_page_url = car_model.css("div div.jet-woo-categories-content div h5 a::attr(href)").get()
            car_model_name = car_model.css("div div.jet-woo-categories-content div h5 a::text").get()'''
            
        for i, car_model_url in enumerate(car_model_urls):

            yield response.follow(car_model_url, callback = self.parse_part_page_initial,
                                  meta = {"car_model": car_models[i]})

    def parse_part_page_initial(self, response):
        car_mark = response.css("nav.woocommerce-breadcrumb a:nth-of-type(2)::text").get()
        car_model = response.meta["car_model"]
        
        nav_list = response.css("nav.jet-woo-builder-shop-pagination")
        if nav_list and nav_list.css("a"):

            nav_1 = list(nav_list.css("span::text").get())
            nav_2 = nav_list.css("a::text").getall()
            page_numbers = nav_1 + nav_2
            
            url_car_name = response.css(".woocommerce-products-header__title::text").get()

            
            for page in page_numbers:
                yield response.follow(f"https://megaautoparts.ge/product-category/{car_mark.lower()}/{adjust_car_name_for_url_megaauto(url_car_name)}/page/{page}/", callback = self.parse_part_page,
                                      meta = {"car_mark": car_mark, "car_model": car_model})
                
    def parse_part_page(self, response):
        part_list = response.css("div.elementor-jet-woo-builder-products-loop .jet-woo-products-wrapper ul.products li")
        
        for part in part_list:
            item = NawilebiItem()
            item["website"] = "https://megaautoparts.ge/"
            item["car_mark"] = response.meta["car_mark"]
            item["car_model"] = response.meta["car_model"]
            item["part_url"] = part.css("div div section div.elementor-container div div div:nth-of-type(1) div div div a::attr(href)").get()
            item["part_full_name"] = part.css("div div section div.elementor-container div div div:nth-of-type(2) div h5 a::text").get()
            price = part.css("div div section div.elementor-container div div div:nth-of-type(3) div div div")
            if price.css("del") or price.css("ins"):
                item["price"] = price.css("ins span bdi::text").get()
                item["original_price"] = price.css("del span bdi::text")
            else:
                item["price"] = part.css("span bdi::text").get()
                
            item["start_year"]= None
            item["end_year"] = None
            item["year"] = None
            
            yield item
    
    
    
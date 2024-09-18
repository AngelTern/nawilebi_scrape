import scrapy


class MegaautopartsSpider(scrapy.Spider):
    name = "megaautoparts"
    allowed_domains = ["megaautoparts.ge"]
    start_urls = ["https://megaautoparts.ge/"]

    def parse(self, response):
        car_mark_list = response.css("#main > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-9bc83c8.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > div > div > div > div > div")
        
        for car_mark in car_mark_list:
            car_model_page_url = car_mark.css("div div.jet-woo-categories-content div h5 a::attr(href)").get()
            car_mark_name = car_mark.css("div div.jet-woo-categories-content div h5 a::text").get()
            
            yield response.follow(car_model_page_url, callback = self.parse_model_page,
                                  meta = {"car_mark": car_mark_name})
            
    def parse_model_page(self, response):
        car_model_list = response.css("#main > div > div > section > div > div > div > div.elementor-element.elementor-element-c875571.elementor-widget.elementor-widget-jet-woo-categories > div > div > div > div")

        for car_model in car_model_list:
            car_parts_page_url = car_model.css("div div.jet-woo-categories-content div h5 a::attr(href)").get()
            car_model_name = car_model.css("div div.jet-woo-categories-content div h5 a::text").get()

            yield response.follow(car_parts_page_url, callback = self.parse_part_page,
                                  meta = {"car_mark": response.meta["car_mark"], "car_model": car_model_name})

    def parse_part_page(self, response):
        car_part_list = response.css("#main > div > div > section.elementor-section.elementor-top-section.elementor-element.elementor-element-193269a.elementor-section-stretched.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default.jet-parallax-section > div.elementor-container.elementor-column-gap-default > div > div > section.elementor-section.elementor-inner-section.elementor-element.elementor-element-7126b8d.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default.jet-parallax-section > div.elementor-container.elementor-column-gap-default > div > div > div.elementor-element.elementor-element-79f2921.elementor-widget.elementor-widget-jet-woo-builder-products-loop > div > div > div > ul > li")
    
        for car_part in car_part_list:
            part_url = car_part.css("div div section div.elementor-container div div div:nth-of-tyep(2) div h5 a::attr(href)").get()
    
    
    
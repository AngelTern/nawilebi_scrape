import scrapy

from nawilebi.items import NawilebiItem


class TopautopartsSpider(scrapy.Spider):
    name = "topautoparts"
    allowed_domains = ["topautoparts.ge"]
    start_urls = ["https://topautoparts.ge/"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            "nawilebi.pipelines.NawilebiPipeline": 100,
            "nawilebi.pipelines.TopaoutopartsPopelines": 200,
            #"nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }


    def parse(self, response):
        
        car_marks = response.css("section.categories__section div.container div.row > div")
        
        for car_mark in car_marks:
            car_mark_url = car_mark.css("div a::attr(href)").get()
            
            yield response.follow(car_mark_url, callback = self.parse_car_mark)

    def parse_car_mark(self, response):
        
        car_models = response.css("div.shop__section div.container div.row div:nth-of-type(2) div div ul li")
        
        for car_model in car_models:
            car_model_url = car_model.css("a::attr(href)").get()
            car_model_name = car_model.css("a div:nth-of-type(2) h2::text").get()
            
            yield response.follow(car_model_url, callback = self.parse_car_model,
                                  meta = {"car_model": car_model_name})
            
    def parse_car_model(self, response):
        car_parts = response.css("div#posts-container > div")
        car_model = response.meta["car_model"]
        
        for car_part in car_parts:
            car_part_url = car_part.css("div div .product-thumb a::attr(href)")
            
            yield response.follow(car_part_url, callback = self.parse_part_page,
                                  meta = {"car_model": car_model})
            
    def parse_part_page(self, response):
        item = NawilebiItem()
        car_model = response.meta["car_model"]
        part_url = response.url
        part_name = response.css("div.product__details--info h2::text").get()
        price = response.css("div.product__details--info div:nth-of-type(1) span::text").get()
        car_mark = response.css("div.product__variant div:nth-of-type(3) div p:nth-of-type(1) span::text").get()

        span_elements_stock = response.css("div.product__variant div:nth-of-type(3) div p:nth-of-type(4) span[style]")
        
        for span in span_elements_stock:
            style = span.attrib.get('style', '')
            span_text = span.css('::text').get().strip()

            item['website'] = "https://topautoparts.ge/"
            item['part_url'] = part_url
            item['car_mark'] = car_mark
            item['part_full_name'] = part_name
            item['car_model'] = car_model
            item['year'] = None
            item['price'] = price
            
            if span_text in ["ბათუმი", "თბილისი"]:
                item['city'] = span_text
                if 'color:red' in style:
                    item['in_stock'] = False
                elif 'color:green' in style:
                    item['in_stock'] = True
                yield item
               
        
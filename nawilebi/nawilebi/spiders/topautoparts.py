import scrapy
from nawilebi.items import NawilebiItem
from utilities.additional_functions import get_digits_after_last_slash, get_digits_after_last_equal
import json


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
            car_mark_id = get_digits_after_last_slash(car_mark_url)
            if car_mark_url:
                yield response.follow(car_mark_url, callback=self.parse_car_mark,
                                      meta = {"car_mark_id": car_mark_id})

    def parse_car_mark(self, response):
        car_models = response.css("div.shop__section div.container div.row div:nth-of-type(2) div div ul li")
        car_mark_id = response.meta["car_mark_id"]
        for car_model in car_models:
            car_model_url = car_model.css("a::attr(href)").get()
            car_model_id = get_digits_after_last_equal(car_model_url)
            car_model_name = car_model.css("a div:nth-of-type(2) h2::text").get()
            if car_model_url and car_model_name:
                yield response.follow(f"https://topautoparts.ge/products_ajax?category_id={car_mark_id}&sub_category={car_model_id}&sort_by=&price_min=&price_max=", callback=self.parse_car_model,
                                      meta={"car_model": car_model_name})

    def parse_car_model(self, response):
        json_data = json.loads(response.text)
        car_model = response.meta["car_model"]
        
        for product in json_data["products"]["data"]:
            product_id = product["id"]
            yield response.follow("https://topautoparts.ge/product_detail/" + str(product_id), callback= self.parse_part_page,
                                  meta = {"car_model": car_model})
            

    def parse_part_page(self, response):
        item = NawilebiItem()

        car_model = response.meta["car_model"]
        part_url = response.url
        part_name = response.css("div.product__details--info h2::text").get()
        price = response.css("div.product__details--info div:nth-of-type(1) span::text").get()
        car_mark = response.css("div.product__variant div:nth-of-type(3) div p:nth-of-type(1) span::text").get()

        if not part_name or not car_mark or not price:
            self.logger.warning(f"Missing data on page: {part_url}")
            return  # Skip if crucial data is missing

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
                item['in_stock'] = 'color:green' in style
                yield item

        self.logger.info(f"Processed part: {part_name} for model: {car_model}")

import scrapy
from nawilebi.items import NawilebiItem

class AutotagiSpider(scrapy.Spider):
    name = "autotagi"
    allowed_domains = ["www.autotagi.ge"]
    start_urls = ["https://www.autotagi.ge/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            #"nawilebi.pipelines.NawilebiPipeline": 100,
            "nawilebi.pipelines.AutotagioPipeline": 200,
            #"nawilebi.pipelines.YearProcessPipeline": 300,
            "nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }
    
    def parse(self, response):
        car_mark_list= response.css("#post-57 > div > section > div.vc_row.wpb_row.vc_row-fluid.vc_custom_1496220814548.vc_row-no-padding > div > div > div > div.vc_row.wpb_row.vc_inner.vc_row-fluid > div")
        
        for car_mark in car_mark_list:
            car_mark_url = response.css("div div div figure a::attr(href)").get()
            
            yield response.follow(car_mark_url, callback = self.parse_mark_page)
            
    def parse_mark_page(self, response):
        car_model_list = response.css("article > div > section > div > div > div > div > div > div > div")
        
        for car_model in car_model_list:
            car_model_url = response.css("div a::attr(href)").get()
            
            yield response.follow(car_model_url, callback = self.parse_part_list)
            
    def parse_part_list(self, response):
        car_mark = response.css("body > div.website-wrapper > div.main-page-wrapper > div.container > div > div > div.shop-loop-head > div.woodmart-woo-breadcrumbs > nav > a.breadcrumb-link.breadcrumb-link-last::text").get()
        car_model = response.css("body > div.website-wrapper > div.main-page-wrapper > div.container > div > div > div.shop-loop-head > div.woodmart-woo-breadcrumbs > nav > span::text").get()
        
        part_list = response.css("body > div.website-wrapper > div.main-page-wrapper > div.container > div > div > div.products.elements-grid.align-items-start.woodmart-products-holder.woodmart-spacing-20.pagination-pagination.row.grid-columns-3 > div")
        
        for part in part_list:
            item = NawilebiItem()
            
            item["part_url"] = part.css("div div:nth-of-type(2) a::attr(href)").get()
            item["part_full_name"] = part.css("div div:nth-of-tope(3) h3 a::text").get()
            item["price"] = part.css("div div:nth-of-tope(3) .product-rating-price div span span bdi::text").get()
            item["car_mark"] = car_mark
            item["car_model"] = car_model
            item["website"] = "https://www.autotagi.ge/"
            item["year"] = None
            item["start_year"] = None
            item["end_year"] = None
            in_stock = part.css("div div:nth-of-type(2) a div")
            
            if in_stock:
                item["in_stock"] = False
            else:
                item["in_stock"] = True
                
            yield item
            
        nav_list = response.css("body > div.website-wrapper > div.main-page-wrapper > div.container > div > div > div.products-footer > nav > ul li")
        
        for nav in nav_list:
            if nav.css("a") and "next" not in nav.css("a::attr(class)").get():
                next_page_url = nav.css("a::attr(href)").get()
                
                yield response.follow(next_page_url, callback = self.parse_next_page,
                                      meta = {"car_model": car_model, "car_mark": car_mark})
                
    def parse_next_page(self, response):
        car_mark = response.meta["car_mark"]
        car_model = response.meta["car_model"]
        
        part_list = response.css("body > div.website-wrapper > div.main-page-wrapper > div.container > div > div > div.products.elements-grid.align-items-start.woodmart-products-holder.woodmart-spacing-20.pagination-pagination.row.grid-columns-3 > div")
        
        for part in part_list:
            item = NawilebiItem()
            
            item["part_url"] = part.css("div div:nth-of-type(2) a::attr(href)").get()
            item["part_full_name"] = part.css("div div:nth-of-tope(3) h3 a::text").get()
            item["price"] = part.css("div div:nth-of-tope(3) .product-rating-price div span span bdi::text").get()
            item["car_mark"] = car_mark
            item["car_model"] = car_model
            item["website"] = "https://www.autotagi.ge/"
            item["year"] = None
            item["start_year"] = None
            item["end_year"] = None
            in_stock = part.css("div div:nth-of-type(2) a div")
            
            if in_stock:
                item["in_stock"] = False
            else:
                item["in_stock"] = True
                
            yield item

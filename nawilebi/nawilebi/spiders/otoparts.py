import scrapy
from nawilebi.items import NawilebiItem
from scrapy_splash import SplashRequest

class OtopartsSpider(scrapy.Spider):
    name = "otoparts"
    allowed_domains = ["otoparts.ge"]

    custom_settings = {
    'ITEM_PIPELINES': {
        # Uncomment and configure your pipelines as needed
        # "nawilebi.pipelines.NawilebiPipeline": 100,
        # "nawilebi.pipelines.CarpartsPipeline": 200,
        # "nawilebi.pipelines.SaveToMySQLPipeline": 900
    },
    'DOWNLOAD_DELAY': 0.5,
    'SPLASH_URL': 'http://localhost:8050',
    'DOWNLOADER_MIDDLEWARES': {
        "nawilebi.middlewares.FakeBrowserHeaderAgentMiddleware": 100,
        'scrapy_splash.SplashCookiesMiddleware': 723,
        'scrapy_splash.SplashMiddleware': 725,
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    },
    'DUPEFILTER_CLASS': 'scrapy_splash.SplashAwareDupeFilter',
    'HTTPCACHE_STORAGE': 'scrapy_splash.SplashAwareFSCacheStorage',
    'SPIDER_MIDDLEWARES': {
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,
    }
}

    
    def start_requests(self):
        url = "https://otoparts.ge/dzaris-natsilebi/"
        yield SplashRequest(url, callback=self.parse)

    def parse(self, response):
        car_mark_urls_list = response.css("div.elementor-177 section > div div div div div a::attr(href)").getall()
        
        for car_mark_url in car_mark_urls_list:
            yield SplashRequest(car_mark_url, callback=self.parse_mark_page)

    def parse_mark_page(self, response):
        car_model_urls = response.css(".elementor-image-box-title a::attr(href)").getall()
        
        for car_model_url in car_model_urls:
            yield SplashRequest(car_model_url, callback=self.parse_model_page)

    def parse_model_page(self, response):
        part_urls = response.css("ul li.product div .premium-woo-products-details-wrap a.premium-woo-product__link::attr(href)").getall()
        
        for part_url in part_urls:
            yield SplashRequest(part_url, callback=self.parse_part_page, meta={'part_url': part_url})

    def parse_part_page(self, response):
        item = NawilebiItem()
        
        item["car_mark"] = response.css("nav.woocommerce-breadcrumb a:nth-of-type(2)::text").get()
        item["car_model"] = response.css("nav.woocommerce-breadcrumb a:nth-of-type(3)::text").get()
        item["part_url"] = response.meta["part_url"]
        item["part_full_name"] = response.css("h1.product_title::text").get()
        item["price"] = response.css("div.elementor-widget-container p.price span.woocommerce-Price-amount bdi::text").get()
        
        in_stock = response.css("div.elementor-add-to-cart p.stock::text").get()
        item["in_stock"] = True if in_stock == "მარაგში" else False
        
        item["website"] = "https://otoparts.ge/"
        item["year"] = None
        item["start_year"] = None
        item["end_year"] = None
        
        yield item

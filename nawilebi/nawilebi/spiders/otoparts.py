import scrapy
from nawilebi.items import NawilebiItem
from scrapy_splash import SplashRequest

class OtopartsSpider(scrapy.Spider):
    name = "otoparts"
    allowed_domains = ["otoparts.ge", "localhost"]

    custom_settings = {
    'ITEM_PIPELINES': {
        # "nawilebi.pipelines.NawilebiPipeline": 100,
        # "nawilebi.pipelines.CarpartsPipeline": 200,
        # "nawilebi.pipelines.SaveToMySQLPipeline": 900
    },
    'DOWNLOAD_DELAY': 2,
    #'CONCONCURRENT_REQUESTS': 1,
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
    lua_start = """
    function main(splash, args)
        assert(splash:go(args.url))
        
        while not splash:select('div.elementor-177 section > div div div div div a') do
            splash:wait(0.1)
            print('waiting...')
        end
        return {html=splash:html()}
    end
    """
    lua_parse = """
    function main(splash, args)
        assert(splash:go(args.url))
        
        while not splash:select('.elementor-image-box-title a') do
            splash.wait(0.1)
            print('waiting...')
        end
        return {html=splash:html()}
    end"""
    
    lua_mark_page = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(0.5))
        return {
            html = splash:html(),
        }
    end
    """

    
    lua_model_page = """
    function main(splash, args)
        assert(splash:go(args.url))
        
        while not splash:select('body > div.elementor.product > div > div > div.elementor-element.e-flex.e-con-boxed.e-con.e-child > div') do
            splash.wait(0.1)
            print('waiting...')
        end
        return {html=splash:html()}
    end
    """
    
    def start_requests(self):
        url = "https://otoparts.ge/dzaris-natsilebi/"
        yield SplashRequest(url, callback=self.parse,
                            endpoint='execute', args={'lua_source': self.lua_start, 'url': url})

    def parse(self, response):
        car_mark_urls_list = response.css("div.elementor-177 section > div div div div div a::attr(href)").getall()
        if not car_mark_urls_list:
            self.logger.warning("No car marks found on %s", response.url)
            return

        for car_mark_url in car_mark_urls_list:
            yield SplashRequest(car_mark_url, callback=self.parse_mark_page,
                                endpoint='execute', args = {"lua_source": self.lua_parse, 'url': car_mark_url})

    def parse_mark_page(self, response):
        model_links = response.css("body > div.elementor > section.elementor-section.elementor-top-section.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > section.elementor-section.elementor-inner-section.elementor-element.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-inner-column.elementor-element > div > div > div > div > div > h1 a::attr(href), body > div.elementor > section.elementor-section.elementor-top-section.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div > div > section.elementor-section.elementor-inner-section.elementor-element.elementor-section-boxed.elementor-section-height-default.elementor-section-height-default > div > div.elementor-column.elementor-inner-column.elementor-element > div > div > div > div > div > h3 a::attr(href)").getall()

        for model_link in model_links:
            yield SplashRequest(model_link, callback= self.parse_model_page,
                                endpoint='execute', args={"lua_source": self.lua_mark_page, 'url': model_link})


    def parse_model_page(self, response):
        part_urls = response.css("ul li.product div .premium-woo-products-details-wrap a.premium-woo-product__link::attr(href)").getall()
        
        for part_url in part_urls:
            yield SplashRequest(part_url, callback=self.parse_part_page, meta={'part_url': part_url},
                                endpoint='execute', args = {"lua_source": self.lua_model_page, 'url': part_url})


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

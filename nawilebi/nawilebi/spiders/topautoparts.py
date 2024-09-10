import scrapy


class TopautopartsSpider(scrapy.Spider):
    name = "topautoparts"
    allowed_domains = ["topautoparts.ge"]
    start_urls = ["https://topautoparts.ge/"]
    
    custom_settings = {
        'ITEM_PIPELINES': {
            "nawilebi.pipelines.NawilebiPipeline": 100,
            "nawilebi.pipelines.TopaoutopartsPopelines": 200,
            "nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }


    def parse(self, response):
        pass

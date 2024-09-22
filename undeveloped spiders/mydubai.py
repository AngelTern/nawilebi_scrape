'''import scrapy


class MydubaiSpider(scrapy.Spider):
    name = "mydubai"
    allowed_domains = ["mydubai.ge"]
    start_urls = ["https://mydubai.ge/"]
    custom_settings = {
        'ITEM_PIPELINES': {
            #"nawilebi.pipelines.NawilebiPipeline": 100,
            #"nawilebi.pipelines.MydubaiPipeline": 200,
            #"nawilebi.pipelines.YearProcessPipeline": 300,
            #"nawilebi.pipelines.SaveToMySQLPipeline": 900
        },
        'DOWNLOAD_DELAY': 0.5,
    }
    
    def parse(self, response):
        ascii_numbers = [ord(char) for char in response.body.decode('latin-1')]
        decoded_content = ''.join([chr(num) for num in ascii_numbers])
        decoded_response = scrapy.Selector(text=decoded_content)
        
        car_mark_list = decoded_response.css("#wrapper > div.site-content > div > div.elementor-element.elementor-element-b965817.e-flex.e-con-boxed.e-con.e-parent.e-lazyloaded > div > div.elementor-element.elementor-element-63233f7.e-con-full.e-flex.e-con.e-child > div.elementor-element.elementor-element-4fe9402.e-flex.e-con-boxed.e-con.e-child > div > div, #wrapper > div.site-content > div > div.elementor-element.elementor-element-b965817.e-flex.e-con-boxed.e-con.e-parent.e-lazyloaded > div > div.elementor-element.elementor-element-63233f7.e-con-full.e-flex.e-con.e-child > div.elementor-element.elementor-element-4a99f4a.e-flex.e-con-boxed.e-con.e-child > div > div")
        for car_mark in car'''
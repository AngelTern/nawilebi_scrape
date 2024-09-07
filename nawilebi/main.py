from scrapy.utils.log import configure_logging
from twisted.internet import reactor

from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from nawilebi.nawilebi.spiders.autopia import AutopiaSpider

def main():
    configure_logging()
    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    
    #for seperate running if needed
    '''
    @defer.inlineCallbacks
    def crawl():
        yield runner.crawl(AutopiaSpider)
        yield runner.crawl(...)
        reactor.stop()
        
    crawl()
    reactor.run()
    '''
    
    
    runner.crawl(AutopiaSpider)
    
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    
    reactor.run()
    
if __name__ == '__main__':
    main()
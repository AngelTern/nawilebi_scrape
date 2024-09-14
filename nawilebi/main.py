import logging
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from nawilebi.spiders.autopia import AutopiaSpider
from nawilebi.spiders.autotrans import AutotransSpider
from nawilebi.spiders.carline import CarlineSpider
from nawilebi.spiders.carparts import CarpartsSpider
from nawilebi.spiders.partscorner import PartscornerSpider
from nawilebi.spiders.topautoparts import TopautopartsSpider
from nawilebi.spiders.vgparts import VgpartsSpider
from nawilebi.spiders.vsauto import VsautoSpider 


def main():
    settings = get_project_settings()

    # Configure logging explicitly
    log_file = settings.get('LOG_FILE', 'scrapy_output.log')
    log_level = settings.get('LOG_LEVEL', 'DEBUG')

    logging.basicConfig(
        filename=log_file,
        level=log_level,
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    configure_logging()  # This will still configure Scrapy's internal logging

    runner = CrawlerRunner(settings)
    
    runner.crawl(AutopiaSpider)
    runner.crawl(AutotransSpider)
    runner.crawl(CarlineSpider)
    runner.crawl(CarpartsSpider)
    runner.crawl(PartscornerSpider)
    runner.crawl(TopautopartsSpider)
    runner.crawl(VgpartsSpider)
    runner.crawl(VsautoSpider)
    
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    
    reactor.run()
    
if __name__ == '__main__':
    main()

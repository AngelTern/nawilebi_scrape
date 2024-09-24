import logging
from scrapy.utils.log import configure_logging
from twisted.internet import reactor
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from nawilebi.spiders.apgparts import ApgpartsSpider
from nawilebi.spiders.autogama import AutogamaSpider
from nawilebi.spiders.autopia import AutopiaSpider
from nawilebi.spiders.autotrans import AutotransSpider
from nawilebi.spiders.bgauto import BgautoSpider
from nawilebi.spiders.carline import CarlineSpider
from nawilebi.spiders.carparts import CarpartsSpider
from nawilebi.spiders.crossmotors import CrossmotorsSpider
from nawilebi.spiders.geoparts import GeopartsSpider
from nawilebi.spiders.goparts import GopartsSpider
from nawilebi.spiders.mmauto import MmautoSpider
from nawilebi.spiders.newparts import NewpartsSpider
from nawilebi.spiders.partscorner import PartscornerSpider
from nawilebi.spiders.pp import PpSpider
from nawilebi.spiders.proauto import ProautoSpider
from nawilebi.spiders.soloauto import SoloautoSpider
from nawilebi.spiders.topautoparts import TopautopartsSpider
from nawilebi.spiders.vgparts import VgpartsSpider
from nawilebi.spiders.vsauto import VsautoSpider
from nawilebi.spiders.zuparts import ZupartsSpider


def main():
    settings = get_project_settings()

    # Explicitly configure logging to write to a separate file
    log_file = 'spider_logs.log'  # You can change this path if needed
    log_level = settings.get('LOG_LEVEL', 'DEBUG')

    logging.basicConfig(
        level=log_level,  # Set log level from settings (default: DEBUG)
        format='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

    # File handler for writing logs to a file
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s [%(name)s] %(levelname)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    ))

    # Add file handler to the root logger
    logging.getLogger().addHandler(file_handler)

    configure_logging()  # Keep Scrapy's internal logging configuration

    runner = CrawlerRunner(settings)

    # Run all the imported spiders
    runner.crawl(ApgpartsSpider)
    runner.crawl(AutogamaSpider)
    runner.crawl(AutopiaSpider)
    runner.crawl(AutotransSpider)
    runner.crawl(BgautoSpider)
    runner.crawl(CarlineSpider)
    runner.crawl(CarpartsSpider)
    runner.crawl(CrossmotorsSpider)
    runner.crawl(GeopartsSpider)
    runner.crawl(GopartsSpider)
    runner.crawl(MmautoSpider)
    runner.crawl(NewpartsSpider)
    runner.crawl(PartscornerSpider)
    runner.crawl(PpSpider)
    runner.crawl(ProautoSpider)
    runner.crawl(SoloautoSpider)
    runner.crawl(TopautopartsSpider)
    runner.crawl(VgpartsSpider)
    runner.crawl(VsautoSpider)
    runner.crawl(ZupartsSpider)

    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run()


if __name__ == '__main__':
    main()

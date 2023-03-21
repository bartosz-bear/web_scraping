import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from quotes.spiders.writers import WritersSpider

process = CrawlerProcess(settings=get_project_settings())
process.crawl(WritersSpider)
process.start()
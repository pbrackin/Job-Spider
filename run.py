from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from job_spider.spiders.job_spider import SO_Spider

process = CrawlerProcess(get_project_settings())
process.crawl(SO_Spider)
#process.crawl(MySpider2)
process.start() # the script will block here until all crawling jobs are finished
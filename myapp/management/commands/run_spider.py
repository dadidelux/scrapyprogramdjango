from django.core.management.base import BaseCommand
from scrapy.crawler import CrawlerProcess
from myapp.scrapy_project.scrapy_project.spiders.hobbies_spider import HobbiesSpider
from scrapy.settings import Settings
from myapp.scrapy_project.scrapy_project import settings as my_settings

class Command(BaseCommand):
    help = 'Run the Scrapy spider'

    def handle(self, *args, **kwargs):
        process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        process.crawl(HobbiesSpider)
        process.start()

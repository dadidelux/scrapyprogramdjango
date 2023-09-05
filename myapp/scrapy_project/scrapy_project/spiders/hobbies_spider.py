import scrapy
from myapp.models import ProductData
from scrapy import signals
import logging

class HobbiesSpider(scrapy.Spider):
    name = "hobbies_spider"
    allowed_domains = ["hobbiesdirect.com.au"]
    start_urls = ["https://hobbiesdirect.com.au/traxxas"]

    total_items_scraped = 0
    total_items_to_scrape = 100  # Set this dynamically if possible

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(HobbiesSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
        return spider

    def item_scraped(self, item, response):
        self.total_items_scraped += 1
        progress = (self.total_items_scraped / self.total_items_to_scrape) * 100
        self.logger.info(f'Scrape Progress: {progress:.2f}%')

    def parse(self, response, is_first_page=True):
        traxxas = response.css('div .p-2')
        for item in traxxas:
            name = item.css('a div::text').get()
            if name:
                name = name.strip()
            else:
                print("Skipping item due to missing name")
                continue

            url = item.css('a::attr(href)').get()

            price = item.css('div .mb-1 b::text').get()
            if price:
                try:
                    price = float(price.replace('$', ''))
                except ValueError as e:
                    logging.error(f"An error occurred while converting price: {e}")
                    price = None

            image_url = item.css('div a img::attr(data-src)').extract_first()

            logging.info(f"Name: {name}")
            logging.info(f"URL: {url}")
            logging.info(f"Price: {price}")
            logging.info(f"Image URL: {image_url}")

            try:
                product_data = ProductData(
                    name=name,
                    url=url,
                    price=price,
                    image_url=image_url,
                )
                product_data.save()
            except Exception as e:
                logging.error(f"An error occurred while saving data to database: {e}")
        
        if is_first_page:
            next_page_selector = 'div ul.pagination li:nth-child(10) a::attr(href)'
        else:
            next_page_selector = 'div ul.pagination li:nth-child(12) a::attr(href)'

        next_page = response.css(next_page_selector).get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, cb_kwargs={'is_first_page': False})

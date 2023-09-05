# import scrapy
# from myapp.models import ProductData
# from scrapy import signals
# import logging

# class HobbiesSpider(scrapy.Spider):
#     name = "hobbies_spider"
#     allowed_domains = ["hobbiesdirect.com.au"]
#     start_urls = ["https://hobbiesdirect.com.au/traxxas"]

#     total_items_scraped = 0
#     total_items_to_scrape = 100  # Set this dynamically if possible

#     #misc
#     @classmethod
#     def from_crawler(cls, crawler, *args, **kwargs):
#         spider = super(HobbiesSpider, cls).from_crawler(crawler, *args, **kwargs)
#         crawler.signals.connect(spider.item_scraped, signal=signals.item_scraped)
#         return spider
    
#     #misc
#     def item_scraped(self, item, response):
#         self.total_items_scraped += 1
#         progress = (self.total_items_scraped / self.total_items_to_scrape) * 100
#         self.logger.info(f'Scrape Progress: {progress:.2f}%')

#     #function for scraping
#     # is_first_page checks the firstpage for pagination purposes
#     # since on the li position of the pagination changes when the page is not anymore at the first page
#     def parse(self, response, is_first_page=True):
#         traxxas = response.css('div .p-2')
#         for item in traxxas:
#             name = item.css('a div::text').get()
#             if name:
#                 name = name.strip()
#             else:
#                 print("Skipping item due to missing name")
#                 continue

#             url = item.css('a::attr(href)').get()
#             # i need to go inside of the url
#                 # then get the reviews, rating, stock

#             price = item.css('div .mb-1 b::text').get()
#             if price:
#                 try:
#                     price = float(price.replace('$', ''))
#                 except ValueError as e:
#                     logging.error(f"An error occurred while converting price: {e}")
#                     price = None

#             image_url = item.css('div a img::attr(data-src)').extract_first()

#             # just want to log the results before saving it to database
#             logging.info(f"Name: {name}")
#             logging.info(f"URL: {url}")
#             logging.info(f"Price: {price}")
#             logging.info(f"Image URL: {image_url}")

#             # start of pushing each scraped info to the model ProductData
#             try:
#                 product_data = ProductData(
#                     name=name,
#                     url=url,
#                     price=price,
#                     image_url=image_url,
#                 )
#                 product_data.save()
#             except Exception as e:
#                 logging.error(f"An error occurred while saving data to database: {e}")
        
#         # start of pagination
#         # we have to look for changes in the li:nth-child changes if not the firstpage
#         if is_first_page:
#             next_page_selector = 'div ul.pagination li:nth-child(10) a::attr(href)'
#         else:
#             next_page_selector = 'div ul.pagination li:nth-child(12) a::attr(href)'

#         # pagination, means if next_page is not None we still load the page until it is set to None or no more pages
#         next_page = response.css(next_page_selector).get()
#         if next_page is not None:
#             yield response.follow(next_page, self.parse, cb_kwargs={'is_first_page': False})


#         def parse(self, response):
#                     url = response.follow(url)
#                     yield scrapy.Request(url, callback = self.parse_dir_contents)

#         def parse_dir_contents(self, response):
#                     item = []
#                     stock = response.css('div .col-auto div span::text').get()
#                     item.append(stock)
#                     #rating = response.css('a div::text').get()
#                     review  = response.css('div .js-scroll-to::text').get()
#                     item.append(review)
#                     yield item


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
            if url:
                yield scrapy.Request(url, callback=self.parse_dir_contents, cb_kwargs={'item': item, 'url': url})
            else:
                logging.error("URL not found")
                continue
        
        # Start of pagination
        if is_first_page:
            next_page_selector = 'div ul.pagination li:nth-child(10) a::attr(href)'
        else:
            next_page_selector = 'div ul.pagination li:nth-child(12) a::attr(href)'

        next_page = response.css(next_page_selector).get()
        if next_page is not None:
            yield response.follow(next_page, self.parse, cb_kwargs={'is_first_page': False})

    def parse_dir_contents(self, response, item, url):
        stock = response.css('div .col-auto div span::text').get()
        review = response.css('div .js-scroll-to::text').get()
        
        name = item.css('a div::text').get().strip()
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
        logging.info(f"Stock: {stock}")
        logging.info(f"Review: {review}")

        try:
            product_data = ProductData(
                name=name,
                url=url,
                price=price,
                image_url=image_url,
                stock=stock,
                review=review,
            )
            product_data.save()
        except Exception as e:
            logging.error(f"An error occurred while saving data to database: {e}")

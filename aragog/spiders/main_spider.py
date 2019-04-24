from urllib.parse import urlparse
import logging
import mysql.connector as dbapi
import scrapy
from scrapy import signals
from scrapy.linkextractors import LinkExtractor
from aragog.logic import site_logic
from aragog.logic import crawl_logic
from aragog.logic import page_logic
from aragog.logic import image_logic
 
class MainSpider(scrapy.Spider):
    name = "main"
    user_name = 'aragog'
    handle_httpstatus_list = [301, 302, 401, 404, 500]
    logger = None
    crawl_id = None
    mydb = None
    
    def __init__(self, *args, **kwargs):
        self.logger = logging.getLogger('aragog')
        self.logger.setLevel(logging.INFO)
        super().__init__(*args, **kwargs)
    
        self.mydb = dbapi.connect(
                host="0.0.0.0",
                user="gsulcer",
                passwd="Qu33n$goodink"
            )

        self.crawl_id = crawl_logic.start_crawl(self.mydb, self.user_name)
        self.logger.info('\n\n*********************\nstarted crawl_id = %s' % self.crawl_id)

    # @classmethod
    # def from_crawler(cls, crawler, *args, **kwargs):
    #     spider = super(MainSpider, cls).from_crawler(crawler, *args, **kwargs)
    #     crawler.signals.connect(spider.spider_closed, signal=signals.spider_closed)
    #     return spider

    def start_requests(self):

        sites = site_logic.load_sites(self.mydb)

        for site in sites:
            if(site.active):
                self.logger.info('starting crawl on %s' % site.domain)
                crawl_logic.start_site_crawl(self.mydb, site.site_id, self.crawl_id, self.user_name)

                url = 'http%s://www.%s' % ('s' if site.use_ssl else '', site.domain)

                page_id = page_logic.insert_page(self.mydb, site.site_id, self.crawl_id, url, None, self.user_name)

                request = scrapy.Request(url=url, callback=self.parse, errback=self.handle_error)
                request.meta['domain'] = site.domain
                request.meta['site_id'] = site.site_id
                request.meta['crawl_id'] = self.crawl_id
                request.meta['page_id'] = page_id

                yield request

    def parse(self, response):
        print('.', end='', flush=True)
        domain = response.meta['domain']
        site_id = response.meta['site_id']
        crawl_id = response.meta['crawl_id']
        page_id = response.meta['page_id']

        response_time = response.meta['download_latency']

        page_logic.update_page(self.mydb, page_id, response.status, response.body, response_time, self.user_name)

        links = LinkExtractor(allow_domains=(domain,)).extract_links(response)
        images = response.css('img::attr(src)').getall()

        for link in links:
            url = urlparse(link.url)
            if(len(url.path) > 2):
                page_id = page_logic.insert_page(self.mydb, site_id, crawl_id, url.path, response.url, self.user_name)
                request = response.follow(link, callback=self.parse, errback=self.handle_error)
                request.meta['domain'] = domain
                request.meta['site_id'] = site_id
                request.meta['crawl_id'] = crawl_id
                request.meta['page_id'] = page_id
                yield request

        for image in images:
            image_id = image_logic.insert_image(self.mydb, site_id, crawl_id, image, response.url, self.user_name)
            request = response.follow(url=image, callback=self.parse_image, errback=self.handle_error)
            request.meta['domain'] = domain
            request.meta['site_id'] = site_id
            request.meta['crawl_id'] = crawl_id
            request.meta['image_id'] = image_id
            yield request

    def parse_image(self, response):
        print('~', end='', flush=True)
        domain = response.meta['domain']
        site_id = response.meta['site_id']
        crawl_id = response.meta['crawl_id']
        image_id = response.meta['image_id']

        response_time = response.meta['download_latency']

        image_logic.update_image(self.mydb, image_id, response.status, response.body, response_time, self.user_name)

    def handle_error(self, failure):
        print('*', end='', flush=True)
        url = urlparse(failure.request.url)
        
        site_id = failure.request.meta['site_id']
        crawl_id = failure.request.meta['crawl_id']
        page_id = failure.request.meta['page_id']

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

            page_logic.update_page(self.mydb, page_id, failure.value.response.status, None, self.user_name)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

            page_logic.update_page(self.mydb, page_id, 997, None, self.user_name)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)

            page_logic.update_page(self.mydb, page_id, 998, None, self.user_name)

        else:
            page_logic.update_page(self.mydb, page_id, 999, None, self.user_name)
        
    def closed(self, reason):
        self.logger.info('\n\n CLOSED %s\n\n' % self.crawl_id)
        crawl_logic.finish_crawl(self.mydb, self.crawl_id, self.user_name)
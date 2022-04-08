from gc import callbacks
import scrapy
from scrapy_selenium import SeleniumRequest

class DealsSpider(scrapy.Spider):
    name = 'deals'

    def start_requests(self):
        yield SeleniumRequest(
            url = 'https://slickdeals.net/computer-deals/',
            wait_time = 3,
            screenshot = True,
            callback = self.parse

        )

    def parse(self, response):
        img = response.meta['screenshot']

        with open('screenshot.png','wb') as f:
            f.write(img)
        

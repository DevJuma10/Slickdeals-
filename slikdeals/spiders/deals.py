import scrapy
from scrapy_selenium import SeleniumRequest
import time

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
        driver = response.meta['driver']
        driver.set_window_size(1920,1080)
        time.sleep(60)
        
        items = response.xpath("//li[@class='fpGridBox grid altDeal hasPrice']")
        for item in items:
            yield{
                "item store"  :  response.xpath(".//span[@class='blueprint']/button/text()").get() ,
                "description"   :  response.xpath(".//a[contains(@class, 'itemTitle bp-p-dealLink bp-c-link')]/text()").get() ,
                "price" :   response.xpath("normalize-space(.//div[@class='itemPrice  wide ']/text())").get()
            }

        # driver.save_screenshot("test.png")
        # driver.close()
        next_page = response.xpath("//*[@id='fpMainContent']/div[6]/a[position() = last()]/@href").get()

        if next_page:
            next_page_url = response.urljoin(next_page)
            yield SeleniumRequest(
                url = next_page_url,
                wait_time = 3,
                callback = self.parse
            )
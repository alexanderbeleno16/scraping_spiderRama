import scrapy


class SpiderramaSpider(scrapy.Spider):
    name = 'spiderRama'
    allowed_domains = ['spiderRama.com']
    start_urls = ['http://spiderRama.com/']

    def parse(self, response):
        pass

import scrapy
from ..items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'douban'
    # allowed_domains = ['movie.douban.com']
    # start_urls = ['http://https://movie.douban.com/chart/']
    #/html/body/div[3]/div[1]/div/div[1]/ol/li
    url = 'https://movie.douban.com/top250?start={}&filter='
    def start_requests(self):
        for sn in range(0,250,25):
            url=self.url.format(sn)
            print(url)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    def parse(self, response):
        print(response.headers['User-Agent'])
        m_list=response.xpath('/html/body/div[3]/div[1]/div/div[1]/ol/li')
        item=DoubanItem()
        for m in m_list:
            item['name']=m.xpath('./div/div[2]/div[1]/a/span[1]/text()').get()
            yield item
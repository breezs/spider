import scrapy
import json
from ..items import SoItem

class SoSpider(scrapy.Spider):
    name = 'so'
    allowed_domains = ['image.so.com']
    # start_urls = ['http://image.so.com/']
    url='https://image.so.com/zjl?ch=beauty&sn={}'
    #多线程，重写start_requests方法
    def start_requests(self):
        #爬取4页的数据
        for sn in range(0,100,30):
            url=self.url.format(sn)
            yield scrapy.Request(
                url=url,
                callback=self.parse_page
            )

    def parse_page(self, response):
        # 将json转换为字典
        html=json.loads(response.text)
        print(html)
        #创建item对象
        item=SoItem()
        for img in html['list']:
            item['img_link']=img['qhimg_url']
            item['img_title']=img['title']
            yield item  #甩给了管道文件



import scrapy
from ..items import DaomuItem

class DaomuSpider(scrapy.Spider):
    name = 'daomu'
    allowed_domains = ['www.daomubiji.com']
    start_urls = ['http://www.daomubiji.com/']

    def parse(self, response):
        # 基准xpath
        a_list=response.xpath('//li[contains(@id,"menu-item-20")]/a')
        print(a_list)
        for a in a_list:
            item=DaomuItem()
            item['title']=a.xpath('./text()').get()
            link=a.xpath('./@href').get()
            yield scrapy.Request(
                url=link,
                meta={'item':item},
                callback=self.parse_two
            )

    #解析二级解析
    def parse_two(self,response):
        #取出解析函数之间的传递函数
        item=response.meta['item']
        article_list=response.xpath('//article')
        for a in article_list:
            name=a.xpath('./a/text()').get()
            two_link=a.xpath('./a/@href').get()
            print(name)
            yield scrapy.Request(
                url=two_link,
                meta={'item':item,'name':name},
                callback=self.parse_three
            )

    #解析三级页面
    def parse_three(self,response):
        item=response.meta['item']
        item['name']=response.meta['name']
        p_list=response.xpath('//article/p/text()').extract()
        #把章节名加在文件开头
        p_list.insert(0,item['name'])
        #再加一行,换行
        content='\n'.join(p_list)
        item['content']=content
        yield item
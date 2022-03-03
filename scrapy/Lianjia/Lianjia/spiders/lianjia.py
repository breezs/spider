import scrapy


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['hz.lianjia.com']
    start_urls = ['https://hz.lianjia.com/ershoufang/']

    def parse(self, response):
        # 获取区县的url
        url_link=['http://hz.lianjia.com'+ i for i in response.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div/a/@href').extract()]
        print(url_link)
        for url in url_link:
            yield scrapy.Request(
                url=url,
                callback=self.parse_two_page
            )

    def parse_two_page(self,response):
        #获取总数
        number=int(response.xpath('/html/body/div[4]/div[1]/div[2]/h2/span/text()').extract()[0])
        print(number)
        #一个页面只能显示3000条，大于3000条的就再整理下属链接再爬取
        if number<=3000:
            page=self.get_pagenumber(number)
            for pg in range(1,page+1):
                url=response.url+'/pg'+str(pg)
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_three_page
                )
        else:#大于3000条的记录需要再次整理区县下属的链接
            url_link=['http://hz.lianjia.com'+i for i in response.xpath('/html/body/div[3]/div/div[1]/dl[2]/dd/div[1]/div[2]/a/@href').extract()]
            for url in url_link:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse_two_page
                )

    def get_pagenumber(self,number):
        page=0
        if number%30>0:
            page=number//30+1
        else:
            page=number//30
        return  page

    def parse_three_page(self,response):
        xp_path = '//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'
        xp_li = response.xpath(xp_path)
        item = {}
        L = []
        # L.append(('title', 'positionInfo', 'totalPrice', 'xpath_unitPrice',
        #           'model', 'area', 'direction', 'zhuangxiu', 'floor', 'create_time', 'floor_type'
        #           ))
        for r in xp_li:
            # '''<a class="" href="https://bj.lianjia.com/ershoufang/101114192790.html" target="_blank" data-log_index="2" data-el="ershoufang" data-housecode="101114192790" data-is_focus="" data-sl="">三环边 您的理想家 南北三居室 明厨明卫</a>'''
            # 1.房屋标题
            xpath_title = r.xpath('.//div[@class="title"]/a/text()').extract()
            print(xpath_title)
            if xpath_title == None:
                continue
            else:
                item['title'] = xpath_title[0].strip()
            # 2获取小区名
            # 注意.//与//区别，.//迭代一次在xpath_positionInfo里面，//将所有迭代后的内容放在xpath_positionInfo里面
            xpath_positionInfo = r.xpath('.//div[@class="positionInfo"]/a[1]/text()').extract()
            item['positionInfo'] = xpath_positionInfo[0].strip() if xpath_positionInfo[0].strip() else None
            print(item['positionInfo'])
            # 3.房屋信息
            xpath_houseInfo = r.xpath('.//div[@class="houseInfo"]/text()')
            houseInfo = xpath_houseInfo.extract()[0].split('|')
            if len(houseInfo) == 7:
                item['model'] = houseInfo[0].strip()
                item['area'] = houseInfo[1].strip()
                item['direction'] = houseInfo[2].strip()
                item['zhuangxiu'] = houseInfo[3].strip()
                item['floor'] = houseInfo[4].strip()
                item['create_time'] = houseInfo[5].strip()
                item['floor_type'] = houseInfo[6].strip()
            else:
                item['model'] = item['area'] = item['direction'] = item['zhuangxiu'] = item['floor'] = item[
                    'create_time'] = item['floor_type'] = None

            # 4.总价
            xpath_totalPrice = r.xpath('.//div[@class="priceInfo"]/div[1]/span/text()').extract()
            item['totalPrice'] = xpath_totalPrice[0].strip() if xpath_totalPrice[0].strip() else None
            # .5.单价
            xpath_unitPrice = r.xpath('.//div[@class="priceInfo"]/div[2]/span/text()').extract()
            item['unitPrice'] = xpath_unitPrice[0][0:-3].strip() if xpath_unitPrice[0][0:-3].strip() else None
            yield item
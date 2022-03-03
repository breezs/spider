#coding:utf-8
# 源码注意li类名的动态刷新
import requests
from lxml import etree
import csv
import time,random
from fake_useragent import UserAgent
class LianJiaSpider:
    def __init__(self):
        #初始URL
        self.url='https://bj.lianjia.com/ershoufang/pg{}/'
        self.number=0

    #获取页面HTML代码
    def get_html(self,url):
        headers={
            'User-Agent': UserAgent().random
        }
        #尝试三次请求，不通就换下一个url
        if self.number<=3:
            try:
                res = requests.get(url=url, headers=headers,timeout=5)
                # res.encoding='utf-8'
                # 获取页面字符串
                html=res.text
                self.parse_html(html)
            except Exception as e:
                print('Retry',self.number,e)
                self.number+=1
                self.get_html(url)
    #解析HTML源代码，得到所需数据
    def parse_html(self,html):
        #设置为xpath可解析格式
        parse=etree.HTML(html)
        #xpath解析表达式
        xp_path='//ul[@class="sellListContent"]/li[@class="clear LOGVIEWDATA LOGCLICKDATA"]'
        #进行解析
        xp_li=parse.xpath(xp_path)
        # 定义字典格式用于保存
        item = {}
        # 定义列表，内容为item字典
        L=[]
        #设置数据名称
        L.append(('title','positionInfo','totalPrice', 'xpath_unitPrice',
                'model', 'area', 'direction', 'zhuangxiu','floor', 'create_time','floor_type'
            ))
        #遍历每个房屋进行解析
        for r in xp_li:
        # '''<a class="" href="https://bj.lianjia.com/ershoufang/101114192790.html" target="_blank" data-log_index="2" data-el="ershoufang" data-housecode="101114192790" data-is_focus="" data-sl="">三环边 您的理想家 南北三居室 明厨明卫</a>'''
            #1.房屋标题
            xpath_title=r.xpath('.//div[@class="title"]/a/text()')
            print(xpath_title)
            item['title']=xpath_title[0].strip()
            # 2获取小区名
            xpath_positionInfo=r.xpath('.//div[@class="positionInfo"]/a[1]/text()')
            item['positionInfo']=xpath_positionInfo[0].strip() if xpath_positionInfo[0].strip() else None
            print(item['positionInfo'])
            #3.房屋信息
            xpath_houseInfo=r.xpath('.//div[@class="houseInfo"]/text()')
            houseInfo= xpath_houseInfo[0].split('|')
            if len(houseInfo)==7:
                item['model']=houseInfo[0].strip()
                item['area'] = houseInfo[1].strip()
                item['direction'] = houseInfo[2].strip()
                item['zhuangxiu'] = houseInfo[3].strip()
                item['floor'] = houseInfo[4].strip()
                item['create_time'] = houseInfo[5].strip()
                item['floor_type'] = houseInfo[6].strip()
            else:
                item['model']= item['area']=item['direction']=item['zhuangxiu']=item['floor']=item['create_time']=item['floor_type']=None

            # 4.总价
            xpath_totalPrice=r.xpath('.//div[@class="priceInfo"]/div[1]/span/text()')
            item['totalPrice']=xpath_totalPrice[0].strip() if xpath_totalPrice[0].strip() else None
            #.5.单价
            xpath_unitPrice=r.xpath('.//div[@class="priceInfo"]/div[2]/span/text()')
            item['unitPrice']=xpath_unitPrice[0][0:-3].strip() if xpath_unitPrice[0][0:-3].strip() else None
            print(item)
            L.append((item['title'],item['positionInfo'], item['totalPrice'], item['unitPrice'],
                item['model'], item['area'], item['direction'], item['zhuangxiu'], item['floor'], item['create_time'],item['floor_type']
            ))
        #保存数据
        self.save_data(L)

    # 保存数据为csv格式
    def save_data(self,L):
        with open('../lianjia.csv', 'w', encoding='utf-8' , newline='') as f:
            writer=csv.writer(f)
            writer.writerows(L)
    #运行
    def run(self):
        #爬取一页
        for pg in range(0,1):
            self.number=1
            #得到url
            url=self.url.format(pg)
            #获取页面并进行解析
            self.get_html(url)
            time.sleep(random.randint(1,3))

if __name__ == '__main__':
    spider=LianJiaSpider()
    spider.run()
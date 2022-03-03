import csv

import requests
import random,time
from  fake_useragent import UserAgent
from lxml import etree

class GuShiWenSpider(object):
    def __init__(self):
        #网站的URL
        self.url='https://so.gushiwen.cn/gushi/tangshi.aspx'

    #得到一级页面
    def get_html(self,url):
        #设置headers
        headers={
            'User-Agent':UserAgent().random
        }
        html=requests.get(url=url,headers=headers).text
        return html


    #解析页面
    def parse_html(self,url):
        item={}
        html=self.get_html(url)
        # xpath匹配元素
        xp_dbs='//div[@class="left"]/div[@class="sons"]/div'
        r_list=self.parse_xpath(xp_dbs,html)
        # 得到各种类型古诗的总列表
        print(r_list)
        for r in r_list:
            #得到古诗类型
            item['type']=r.xpath('.//div[1]/strong/text()')[0].strip()
            # 得到每个类型下的所有古诗列表
            span_list=r.xpath('.//span')
            time.sleep(random.randint(1,3))
            for s in span_list:
                href=s.xpath('.//a/@href')[0]
                # 得到每首古诗的二级页面
                two_url='https://so.gushiwen.cn'+href
                #解析二级页面
                item['name'],item['auther'],item['text']=self.parse_two_html(two_url)
                L=[item['type'],item['name'],item['auther'],item['text']]
                # 保存古诗为csv
                self.save_text(L)
                time.sleep(random.randint(1, 3))
                print(item)



    #解析二级页面
    def parse_two_html(self,two_url):
        html=self.get_html(two_url)
        name_dbs='//h1/text()'
        name=self.parse_xpath(name_dbs,html)[0].strip()
        auther=self.parse_xpath('//div[@class="main3"]/div/div[2]/div/p/a[1]/text()',html)[0].strip()
        print(auther)
        # 得到的是数组，格式有问题，需要整理一下
        text_list=self.parse_xpath('//div[@class="main3"]/div/div[2]/div/div/text()',html)[-2:]
        text=''
        for r in text_list:
            r=r.strip()
            text=text+r
        print(text)
        return name,auther,text

    #保存古诗
    def save_text(self,L):
        with open('gushici.csv','a',encoding='utf-8',newline='') as f:
            writer=csv.writer(f)
            writer.writerow(L)

    #xpath解析方法
    def parse_xpath(self,xp_dbs,html):
        xp_html=etree.HTML(html)
        r_list=xp_html.xpath(xp_dbs)
        return r_list

    def run(self):
        url=self.url
        self.parse_html(url)
if __name__ == '__main__':
    spider=GuShiWenSpider()
    spider.run()

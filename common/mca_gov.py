import csv
from hashlib import md5
import requests
import re
import time
import random
import pymysql
from lxml import etree
from fake_useragent import UserAgent
class ZfSpider(object):
    #初始化URL以及url以及连接数据库
    def __init__(self):
        self.url='http://www.mca.gov.cn/article/sj/xzqh/2020/'
        self.headers={'User-Agent':UserAgent().random}
        self.db=pymysql.connect(host='localhost',user='root',password='123456',database='zfdb',charset='utf8')
        self.cursor = self.db.cursor()
    # 获取最新的行政区划分码，该网站获得的URL是假的，需要在该页面中去再次获取URL
    def get_false_url(self):
        #得到页面
        html=requests.get(url=self.url,headers=self.headers).text
        #替换注释，防止xpath不能解析
        html = html.replace('<!--', '').replace('-->', '')
        xp_dbs='//a[@class="artitlelist"]'
        parse_html=etree.HTML(html)
        # 得到所有的页面的列表
        a_link=parse_html.xpath(xp_dbs)
        # 遍历，判断标题中是否含有"代码"
        for a in a_link:
            text=a.xpath('./text()')[0].strip()
            href=a.xpath('./@href')[0].strip()
            #判断标题中是否含有"代码"，我们只需要爬取含有的”代码页“
            if text.endswith('代码'):
                false_url='http://www.mca.gov.cn'+href
                #判断是否有指纹,
                if self.is_finger(false_url):
                    self.get_true_url(false_url)
                    self.save_url(text, false_url)  # 保存假链接
                    break
                else:
                    print('已经下载了')
                    break
    #获取响应内容，分析js，提取真实url
    def get_true_url(self,false_url):
        html=requests.get(
            url=false_url,
            headers=self.headers
        ).text
        pattern=re.compile('window.location.href="(.*?)";.*?')
        true_link=pattern.findall(html)[0].strip()
        print(true_link)
        #解析页面，获取区县
        self.parse_html(true_link)

    # 解析页面，获取区县
    def parse_html(self,true_link):
        html = requests.get(url=true_link, headers=self.headers).text
        parse_html=etree.HTML(html)
        tr_list=parse_html.xpath('//tr[@height="19"]')
        #存到csv
        # L=[('name','code')]
        # with open('zfdata.csv','w',encoding='utf-8',newline='') as f:
            # writer=csv.writer(f)
        for tr in tr_list:
            code=tr.xpath('./td[2]/text() | ./td[2]/span/text()' )[0].strip()
            name=tr.xpath('./td[3]/text()')[0].strip()
            print(name,code)
            # 存入到数据库
            self.save_mysql(name,code)
                # L.append((name,code))
            # writer.writerows(L)

    #判断省市县，并进行分表保存
    def save_mysql(self,name,code):
        if code[2:]=='0000':#省
            self.save_data('province',name,code)
        elif code[4:]=='00':#市
            self.save_data('city',name,code)
        else: #县
            self.save_data('country',name,code)

    #保存
    def save_data(self,table,name,code):
        if table=='province':
            sql='insert into '+table +' value(%s,%s)'
            self.cursor.execute(sql,[code,name])
        else:
            sql=sql='insert into '+table +' value(%s,%s,%s)'
            if table=='city':
                self.cursor.execute(sql, [code,code[:2]+'0000' ,name])
            else:
                self.cursor.execute(sql, [code, code[:4] + '00', name])
        self.db.commit()

    # 5.判断指纹函数
    def is_finger(self, false_url):
        #md5加密
        s = md5()
        s.update(false_url.encode())
        finger = s.hexdigest()
        #查询是否有该加密码
        sql = 'select url from finger where url=%s'
        r = self.cursor.execute(sql, [finger])
        #没有就返回True
        if not r:
            return True

    #保存指纹
    def save_url(self,text,false_url):
        # 把指纹保存到数据库中
        s = md5()
        s.update(false_url.encode())
        url_finger = s.hexdigest()
        #sql语句
        sql = 'insert into finger values(%s,%s)'
        self.cursor.execute(sql, [text,url_finger])
        self.db.commit()

if __name__ == '__main__':
    spider=ZfSpider()
    spider.get_false_url()
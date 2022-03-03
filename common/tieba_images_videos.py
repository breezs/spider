import time
import random
import requests
from fake_useragent import UserAgent
import re
import csv
from urllib import parse
import os
from lxml import etree
class TieBaSpider(object):
    #定义网站的url
    def __init__(self):
        self.url='https://tieba.baidu.com/f?kw={}&pn={}'
        self.name=''

    # 获取html
    def get_html(self,url):
        headers={
            'User-Agent': UserAgent().random,
            'cookie': 'BIDUPSID=59F8E699FD2C39D60B9CF3028DD93C71; PSTM=1642739906; __yjs_duid=1_02ba4a01a053c2c99f48c0ef66bb3cd41642826075514; BAIDUID=129A17B69212E526887BB08A61716A0F:FG=1; BDUSS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDUSS_BFESS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=8DE223F09137022DEC851A1440ACE714:FG=1; BAIDU_WISE_UID=wapp_1645611718515_366; ab_sr=1.0.1_YWM3ZDQ2ZjZiMTQ5ZmMzOTUyMWNiMTY1Y2M4NjEyNjBlMWI2Y2ZjNDY1ODk1NzRjYWVmNzM1ODk5OTQ5YWIzMDkzNjY3ZTQ5YzY2ZjM3NGExYzJkZjkyNjUzNTU5MWE2NTdiMjY5NWYyM2MxYzcxZmU0NGIwMmRhZDI3MzJmZjBlMTUwMDU1NDBkZmMwZTk0ZmU3ODIyZDc5N2FmZjUxNzRhNDhhMmJiNTJlNGU0YTQyNDJlNTEyOGI4ZjQ0NDZl'
        }
        res=requests.get(url=url,headers=headers)
        res.encoding='utf-8'
        html=res.text
        return html

    # 解析html
    def parse_html(self,one_url):
        # 得到一级页面html文件
        html=self.get_html(one_url)
        print(html)
        # 获取各贴子子链接
        xpath_dbs='//a[@class="j_th_tit "]/@href'
        # 坑：爬取到html被注释掉了,xpath无法解析，需要先取消注释
        html = html.replace('<!--', '').replace('-->', '')
        # 调用xpath解析得到结果
        xp_list=self.xpath_func(html,xpath_dbs)
        # print(xp_list)
        for x in xp_list:
            # 得到拼接子链接，原链接不全
            two_url='https://tieba.baidu.com'+x
            # 保存图片
            print(two_url)
            self.get_sources(two_url)
            # 休息1~3秒
            time.sleep(random.randint(1,3))

    def get_sources(self,url):
        html=self.get_html(url)
        # 反反爬：防止源代码被注释
        html = html.replace('<!--', '').replace('-->', '')
        xpath_dbs='//div[@class="j_ueg_post_content p_forbidden_tip"]/following-sibling::div[1]/img[@class="BDE_Image"]/@src'
        # 得到链接列表
        s_list=self.xpath_func(html,xpath_dbs)
        print(s_list)
        #将每个图片链接去获取图片文件，然后保存
        for i in s_list:
            self.save_source(link=i)

        # 由资源url保存图片和视频
    def save_source(self, link):
        # 得到图片链接页面
        image_html=requests.get(
            url=link,
            headers={'User-Agent': UserAgent().random}
        ).content
        # 命名保存
        #如果是视频
        if ('mp4') in link:
            #创建目录
            dir = self.name + '/videos/'
            if not os.path.exists(dir):
                os.makedirs(dir)
            filename = dir  + link.split('/')[-1].split('?')[0]
        #如果是图片
        else:
            dir = self.name + '/images/'
            if not os.path.exists(dir):
                os.makedirs(dir)
            filename = dir +link.split('/')[-1]
        with open(filename, 'wb') as f:
            f.write(image_html)
            print('下载成功',filename)
        time.sleep(random.randint(1, 3))

    # xpath解析方法
    def xpath_func(self,html,xpath_dbs):
        xpath_html=etree.HTML(html)
        r_list=xpath_html.xpath(xpath_dbs)
        return r_list

    # 运行方法
    def run(self,word,page):
        self.name=word
        # 将关键词进行编码
        word=parse.quote(word)
        one_url=self.url.format(word,page)
        #进行解析
        self.parse_html(one_url)
        #延时，防止被检测到爬虫
        time.sleep(random.randint(1,3))
if __name__ == '__main__':
    spider=TieBaSpider()
    word=input('请输入贴吧名字：')
    start=int(input('请输入起始页：'))
    end=int(input('请输入终止页：'))
    #按输入的页数进行爬取
    for page in range(start,end+1):
        spider.run(word,(page-1)*50)
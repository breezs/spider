import random
import re
import time
from fake_useragent import UserAgent
import requests
import json
# one_url=https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1645709949954&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword=python&pageIndex=1&pageSize=10&language=zh-cn&area=cn
# two_url=https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1645710145851&postId=1476438696285708288&language=zh-cn
class TencentSpider(object):
    #初始化
    def __init__(self):
        self.keyword=''
        self.one_url='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp={}&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
        self.two_url='https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp={}&postId={}&language=zh-cn'
        self.f=open('../day11/tencent.json', 'a', encoding='utf-8')
        self.item_list=[]

    #获取响应内容
    def get_page(self,url):
        headers={'User-Agent':UserAgent().random}
        res=requests.get(url=url,headers=headers)
        res.encoding='utf-8'
        html=res.text
        # json转成python字典
        html_py=json.loads(html)
        return html_py

    def parse_page(self,one_url):
        #得到一级页面，json格式
        one_html_py=self.get_page(one_url)
        #Posts对应每个工作的数据内容
        for job in one_html_py['Data']['Posts']:
            item={}
            # 取postId
            post_id=job['PostId']
            # 拼接二级地址
            two_url=self.two_url.format(time.time()*1000,post_id)
            #解析二级页面，得到工作数据
            item['name'],item['duty'],item['require']=self.parse_two_page(two_url)
            # 存到item字典里面
            self.item_list.append(item)
            print(item)

    # 解析二级页面函数
    def parse_two_page(self,two_url):
        headers = {'User-Agent': UserAgent().random}
        two_html = self.get_page(two_url)
        name=two_html['Data']["RecruitPostName"].replace('\n','')
        duty=two_html['Data']["Responsibility"].replace('\n','')
        require=two_html['Data']["Requirement"].replace('\n','')
        return name,duty,require

    #获取总页数
    def get_numbers(self):
        #总数在第一页的json数据中
        url=self.one_url.format(time.time()*100,self.keyword,1)
        html=self.get_page(url)
        number=int(html["Data"]["Count"])
        if number/10==0:
            number=number/10
        else:
            number=int(number/10)+1
        return number

    def main(self):
        self.keyword=input('请输入职务类别')
        #获取工作总数量
        number=self.get_numbers()
        print(number)
        for page in range(1,3):
            print(f'第{page}页')
            one_url=self.one_url.format(time.time()*100,self.keyword,page)
            self.parse_page(one_url)
            time.sleep(random.randint(1,3))
        #存为json文档
        json.dump(self.item_list,self.f,ensure_ascii=False)

if __name__ == '__main__':
    spider=TencentSpider()
    spider.main()
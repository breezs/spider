import requests
import time,random
import re
from fake_useragent import UserAgent

class DoubanSpider(object):
    #初始胡URL
    def __init__(self):
        self.url='https://movie.douban.com/j/chart/top_list?'
        self.i=0
    def main(self):
        #获取所有电影类型和编号
        type_dict,menu=self.get_all_type_films()
        #主菜单
        menu+=menu+'\n请做出选择:'
        #输入爬取电影类型
        type_name=input(menu)
        #得到类型的编号，用于获取各种类型的url
        type_number=type_dict[type_name]
        # 得到每种类型的总数
        total=self.total_number(type_number)
        print('总数:',total)
        #遍历每页电影
        for start in range(0,(total+1),20):
            params={
                'type':type_number,
                'interval_id':'100:90',
                'start':str(start),
                'limit':'20'
            }
            #获取每页电影
            self.get_page(params,type_name)
            time.sleep(random.randint(1,3))
            print('电影数量：',self.i)

    #
    def get_all_type_films(self):
        #首页的url
        url='https://movie.douban.com/chart'
        html=requests.get(url=url,headers={'User-Agent': UserAgent().random}).text
        # 正则解析
        re_dbs='<a href=.*?type_name=(.*?)&type=(.*?)&interval_id.*?'
        pattern=re.compile(re_dbs,re.S)
        # 得到所有电影类型
        r_list=pattern.findall(html)
        type_dic={}
        menu=''
        for r in r_list:
            #每种类型对应的编号，得到一个字典。
            type_dic[r[0].strip()]=r[1].strip()
            menu+=r[0].strip()+'|'
        return type_dic,menu

    #获取电影总数
    def total_number(self,type_number):
        url=f'https://movie.douban.com/j/chart/top_list_count?type={type_number}&interval_id=100%3A90'
        html = requests.get(url=url, headers={'User-Agent': UserAgent().random}).json()
        print(html)
        total=int(html['total'])
        return total

    #获取页面，以传参的形式
    def get_page(self,params,type_name):
        res=requests.get(url=self.url,params=params, headers={'User-Agent': UserAgent().random})
        html=res.json()
        self.parse_html(html,type_name)

    #解析json格式的数据，得到所需要的数据
    def parse_html(self,html,type_name):
        item={}
        for one in html:
            item['type']=type_name
            item['name']=one['title'].strip()
            item['score'] = one['score'].strip()
            print(item)
            # 页数加一
            self.i+=1
if __name__ == '__main__':
    spider=DoubanSpider()
    spider.main()

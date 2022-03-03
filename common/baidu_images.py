import re
import os
import requests
import fake_useragent as fua
from urllib import parse
# "thumbURL":"https://img0.baidu.com/it/u=3631270939,3946543578&fm=253&fmt=auto&app=120&f=JPEG?w=500&h=1060","adType":"0"
class BaiduImageSpider(object):
    def __init__(self):
        #百度图片的URL地址
        self.url='https://image.baidu.com/search/index?tn=baiduimage&ipn=r&ct=201326592&cl=2&lm=-1&st=-1&fm=result&fr=&sf=1&fmq=1645529107438_R&pv=&ic=0&nc=1&z=0&hd=0&latest=0&copyright=0&se=1&showtab=0&fb=0&width=&height=&face=0&istype=2&dyTabStr=MCwzLDYsMSwyLDQsNSw4LDcsOQ%3D%3D&ie=utf-8&sid=&word={}'

    def get_images(self,url,word):
        #配置User-Agent，必须配置Cookie
        headers = {'User-Agent': fua.UserAgent().random,
                   # 注意cookie反爬
                   'cookie':'BIDUPSID=59F8E699FD2C39D60B9CF3028DD93C71; PSTM=1642739906; __yjs_duid=1_02ba4a01a053c2c99f48c0ef66bb3cd41642826075514; BAIDUID=129A17B69212E526887BB08A61716A0F:FG=1; BDUSS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDUSS_BFESS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=8DE223F09137022DEC851A1440ACE714:FG=1; userFrom=cn.bing.com; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; ab_sr=1.0.1_MzFiOTA0ZDE1NjlkMWI4NjljNjBlOWU3ZGMxMDc3ZDM3YjI4MTdhMWI1OTk3YjA4Y2NjNTYwOTA2ZjEzN2I3ZDNkMGM3Y2MyYjQ0YzQ0ZmYzYTVjZmUxZjFkNjczZTM3NzJiMjk1YWM3ZWY1ZGI0M2Y2Nzg4NzZjMTAxNTg0OTU2NWE4MjY4N2Y1YTBhN2NiYjhlZTEyMzhhOTRjMGEyZDEwMDk4Y2JmYzI5NmRkMWI4NGEwYjA5ZDVlMTIxMzky'
                   }
        res = requests.get(url=url, headers=headers)
        res.encoding='utf-8'
        html=res.text
        #正则匹配
        re_dbs='"thumbURL":"(.*?)"'
        pattern=re.compile(re_dbs,re.S)
        # 得到所有图片的url
        image_link=pattern.findall(html)
        print(image_link)

        # 创建目录
        dir='{}/'.format(word)
        if not os.path.exists(dir):
            os.makedirs(dir)
        #按序号进行命名
        i=1
        for img_l in image_link:
            filename='{}{}_{}.jpg'.format(dir,word,i)
            self.save_images(img_l,filename)
            i+= 1

    #保存图片
    def save_images(self,img_l,filename):
        headers = {'User-Agent': fua.UserAgent().random,
                   'cookie': 'BIDUPSID=59F8E699FD2C39D60B9CF3028DD93C71; PSTM=1642739906; __yjs_duid=1_02ba4a01a053c2c99f48c0ef66bb3cd41642826075514; BAIDUID=129A17B69212E526887BB08A61716A0F:FG=1; BDUSS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDUSS_BFESS=c3dVY5aHhjNlkxaVpXcXllTUNDNTk4T0VnYlQyaXlrbExPU1pCRnZSWW13anRpSVFBQUFBJCQAAAAAAAAAAAEAAADINSPwenNodWFpMDkyNgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACY1FGImNRRiaF; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BAIDUID_BFESS=8DE223F09137022DEC851A1440ACE714:FG=1; userFrom=cn.bing.com; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; ab_sr=1.0.1_MzFiOTA0ZDE1NjlkMWI4NjljNjBlOWU3ZGMxMDc3ZDM3YjI4MTdhMWI1OTk3YjA4Y2NjNTYwOTA2ZjEzN2I3ZDNkMGM3Y2MyYjQ0YzQ0ZmYzYTVjZmUxZjFkNjczZTM3NzJiMjk1YWM3ZWY1ZGI0M2Y2Nzg4NzZjMTAxNTg0OTU2NWE4MjY4N2Y1YTBhN2NiYjhlZTEyMzhhOTRjMGEyZDEwMDk4Y2JmYzI5NmRkMWI4NGEwYjA5ZDVlMTIxMzky'
                   }
        res = requests.get(url=img_l, headers=headers)
        #图片格式必须使用content
        html=res.content
        #存入图片
        with open(filename,'wb') as f:
            f.write(html)
        print(filename,'下载成功')

    def run(self):
        word=input('请输入人名：')
        word_parse=parse.quote(word)
        url=self.url.format(word_parse)
        self.get_images(url,word)

if __name__ == '__main__':
    spider=BaiduImageSpider()
    spider.run()


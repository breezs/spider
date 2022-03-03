import json

import scrapy
from ..items import YoudaoItem
import time,random
from hashlib import md5
class YoudaoSpider(scrapy.Spider):
    name = 'youdao'
    allowed_domains = ['fanyi.youdao.com']
    # start_urls = ['http://fanyi.youdao.com/']
    word=input('请输入要翻译的单词')
    def start_requests(self):
        salt, sign, lts,bv = self.get_salt_sign_lts(self.word)
        post_url='https://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
        cookies=self.get_cookie()
        data = {
            "i": self.word,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": salt,
            "sign": sign,
            "lts": lts,
            # "bv": '2d35addbac4c495364cf10475964cdd9',
            "bv": bv,
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME",
        }
        yield scrapy.FormRequest(
            url=post_url,
            formdata=data,
            callback=self.parse,
            # cookies=cookies

        )

    def get_salt_sign_lts(self,word):
        # js r = "" + (new Date).getTime()
        ts = str(int(time.time() * 1000))

        # 求salt i = r + parseInt(10 * Math.random(), 10);
        salt = ts + str(random.randint(1, 9))

        # n.md5("fanyideskweb" + e + i + "Ygy_4c=r#e#4EX^NUGUc5")
        string = 'fanyideskweb' + word + salt + "Ygy_4c=r#e#4EX^NUGUc5"
        s = md5()
        s.update(string.encode())
        sign = s.hexdigest()
        s2 = md5()
        s2.update(
            '5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 Edg/98.0.1108.56'.encode())
        bv = s2.hexdigest()
        return salt,sign,ts,bv

    def get_cookie(self):
        cs='OUTFOX_SEARCH_USER_ID=-2094518326@10.110.96.159; OUTFOX_SEARCH_USER_ID_NCOO=654528686.5393351; JSESSIONID=aaabc05LV06Lq7Stpyd9x; ___rl__test__cookies=1646102934467'
        cs_list=cs.split(';')
        cs_dict={}
        for c in cs_list:
            cs_dict[c.split('=')[0]]=c.split('=')[1]
        return cs_dict
    def parse(self, response):
        item=YoudaoItem()
        html=json.loads(response.text)
        print(html)
        item['result']=html['translateResult'][0][0]['tgt']
        yield item
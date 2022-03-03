import scrapy
from urllib import parse
import json
from ..items import TencentItem
from scrapy_redis.spiders import RedisSpider
#将scrapy.spiders换为RedisSpider
class TencentSpider(RedisSpider):
    name = 'tencent'
    allowed_domains = ['careers.tencent.com']
    one_url='https://careers.tencent.com/tencentcareer/api/post/Query?timestamp=1645942271770&countryId=&cityId=&bgIds=&productId=&categoryId=&parentCategoryId=&attrId=&keyword={}&pageIndex={}&pageSize=10&language=zh-cn&area=cn'
    two_url='https://careers.tencent.com/tencentcareer/api/post/ByPostId?timestamp=1645942337108&postId={}&language=zh-cn'
    user_input=input('请输入岗位：')
    user_input=parse.quote(user_input)
    # url=one_url.format(user_input,1)
    # start_urls = [url]   #redis改写,去掉start_urls
    #第二步定义redis_key
    redis_key='tencent:spider'
    number=0
    def parse(self, response):
        html=response.text
        #json转为字典格式
        html=json.loads(html)
        for job in html['Data']['Posts']:
            post_id=job['PostId']
            url=self.two_url.format(post_id)
            yield scrapy.Request(
                url=url,
                callback=self.parse_two_page
            )

        #不好理解,且爬取的数据混乱
        total=self.get_page(response)
        for index in range(2,5):
            self.number += 1
            print(f'第{index}页')
            url=self.one_url.format(self.user_input,index)
            yield scrapy.Request(
                url=url,
                callback=self.parse
            )
    def get_page(self,response):
        html = response.text
        # json转为字典格式
        html = json.loads(html)
        # 获取总页数
        count = html['Data']['Count']
        if count % 10 == 0:
            total = count // 10
        else:
            total = count // 10 + 1
        return total

    def parse_two_page(self,response):
        html=json.loads(response.text)['Data']
        item=TencentItem()
        item['job_name']=html['RecruitPostName']
        item['job_type']=html['CategoryName']
        item['job_duty']=html['Responsibility']
        item['job_require']=html['Requirement']
        item['job_address']=html['LocationName']
        item['job_time']=html['LastUpdateTime']
        yield item

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from scrapy.pipelines.images import ImagesPipeline
import scrapy

#继承管道类ImagesPipeline类
class SoPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(item)
        yield scrapy.Request(
            url=item['img_link'],
            meta= {'title':item['img_title']}
        )
    def file_path(self, request, response=None, info=None, *, item=None):
        title=request.meta['title']
        filename = title + "." + request.url.split('.')[-1]
        return filename
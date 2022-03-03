# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

class DaomuPipeline:
    def process_item(self, item, spider):
        #c=创建文件夹
        dir='{}/'.format(item['title'])
        if not os.path.exists(dir):
            os.makedirs(dir)
        filename=dir+item['name'].replace('?','')+'.txt'
        with open(filename,'w',encoding='utf-8') as f:
            f.write(item['content'])
        return item

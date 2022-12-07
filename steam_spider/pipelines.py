# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class SteamSpiderPipeline:
    def open_spider(self, spider):
        self.file = open('items.json', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        if item['release_date'] != "Unknown" and 'Coming' not in item['release_date'] \
                and int(item['release_date'][-4:]) > 2000:
            line = json.dumps(ItemAdapter(item).asdict(), ensure_ascii=False) + '\n'
            self.file.write(line)






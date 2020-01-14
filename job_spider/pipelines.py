# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo

from scrapy.exceptions import DropItem
import logging as log
from scrapy.utils.project import get_project_settings as settings
from datetime import datetime


class JobSpiderPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline:

    def __init__(self):

        connection = pymongo.MongoClient(
            settings().get('MONGODB_SERVER'),
            settings().get('MONGODB_PORT')
        )
        db = connection[settings().get('MONGODB_DB')]
        self.collection = db[settings().get('MONGODB_COLLECTION')]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            # Upserts!
            self.collection.update_one(
                {"provider": item['provider'], "id": item['id']},
                {
                    "$setOnInsert": {"dt_pulled": item['dt_pulled']},
                    "$set": {"dt_updated": datetime.now()},
                },
                upsert=True,
            )
            log.info("Item added tp MongoDB database!")
        return item

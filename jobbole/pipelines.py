# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import codecs
import json
import logging

import pymysql as pymysql
import scrapy.exporters
from scrapy.exporters import CsvItemExporter
from scrapy.pipelines.images import ImagesPipeline
from twisted.enterprise import adbapi
from jobbole.utils.common import join


class JobbolePipeline:

    def process_item(self, item, spider):
        return item


class JoboleImagesPipeline(ImagesPipeline):

    def item_completed(self, results, item, info):
        '''
        默认的item_complete是将结果保存在字段item[IMAGES_RESULT_FIELD]
        自定义下载图片完成后，提取对应的path到item的字段img_url上
        :param results: 下载完成后的结果，为list
                 [(True,
                 {'url': 'http://www.jobbole.com/d/file/p/2019/12-08/6fe07f7b307a065d0d76283fb2dd312d.png',
                 'path': 'full/cb875ccbfaa57dedd4556218f690fb696ae5852c.jpg',
                 'checksum': '8f8641032014b047d06d4b21b94f4284',
                 'status': 'uptodate'}
                 )]
        :param item: 返回的item
        :param info: scrapy.pipelines.media.MediaPipeline.SpiderInfo对象,包含spider对象，downloading正在下载的和downloaded已经完成下载的西悉尼
            {
                "spider":spider,
                "downloading": {xx,xx}, # xx为下载时对img url的hash值
                "downloaded" : {
                        "xx" : {
                            url
                            path
                            checksum
                            status
                        }
                }
            }
        :return:
        '''

        item[self.images_result_field] = [ result.get('path') for ok,result in results if ok ]

        return item


class ArticleCsvPipeline:
    def __init__(self,path):
        self.path = path

    @classmethod
    def from_crawler(cls,crawler):
        return cls(path=crawler.settings["CSV_FILE_PATH"])

    def open_spider(self,spider):
        self.file = open(self.path,'wb+')
        self.exporter = scrapy.exporters.CsvItemExporter(file=self.file,encoding='utf-8-sig')
        self.exporter.start_exporting()

    def process_item(self,item,spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()


class ArticleMysqlPipeline:

    def __init__(self,pool):
        self.pool = pool

    @classmethod
    def from_crawler(cls,crawler):
        adbparams = dict(
            host=crawler.settings['MYSQL_HOST'],
            db=crawler.settings['MYSQL_DB'],
            user=crawler.settings['MYSQL_USER'],
            password=crawler.settings['MYSQL_PASSWORD'],
            cursorclass = pymysql.cursors.DictCursor
        )

        # 初始化数据库连接池
        dbpool = adbapi.ConnectionPool('pymysql',**adbparams)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 执行异步操作，指定异步函数为self.insert，传递的数据为item
        # 调用self.insert时传入的第一个参数为cursor，第二个为item
        query = self.pool.runInteraction(self.insert,item)
        # 添加异常处理，指定异常处理函数,会将异常传入
        query.addErrback(self.handle_error)

    def insert(self,cursor,item):
        insert_sql = '''
        insert into article_details(title,create_date,tags,img_url,content,url) values (%s,%s,%s,%s,%s,%s)
        '''
        data=(item['title'], item['create_date'], item['tags'], item['img_urls'], item['content'], item['url'])
        # twisted 会自动帮我们commit，不需要显式commit
        cursor.execute(insert_sql,data)

    def handle_error(self,err):
        if err:
            logging.basicConfig()
            logging.error(f"insert data to mysql failed with err:{err}")

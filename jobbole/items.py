# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import itemloaders.processors
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join,Compose,MapCompose
from w3lib.html import remove_tags

from jobbole.utils.common import date_from_datetimestr

class JobboleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ArticleItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    create_date_in = MapCompose(date_from_datetimestr)

    # img_urls必须是list，因此不能使用默认的processor
    img_urls_out = itemloaders.processors.Identity()
    # tags需要将值使用","链接
    tags_out = Join(",")

class JobboleArticleItem(scrapy.Item):
    title = scrapy.Field()
    create_date = scrapy.Field()
    url = scrapy.Field()
    img_urls = scrapy.Field()
    tags = scrapy.Field()
    content = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = '''
                insert into article_details(title,create_date,tags,img_url,content,url) values (%s,%s,%s,%s,%s,%s)
                '''
        data = (
        self['title'], self['create_date'], self.get('tags', 'null'), ",".join(self['img_urls']), self['content'],
        self['url'])

        return insert_sql,data

class LagouPositionItemLoader(ItemLoader):
    default_output_processor = TakeFirst()

    tags_out = Join(",")

class LagouPositionItem(scrapy.Item):

    job_name = scrapy.Field()
    url = scrapy.Field()
    company = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    experience = scrapy.Field()
    degree = scrapy.Field()
    job_catagory = scrapy.Field()
    tags = scrapy.Field()
    publish_date = scrapy.Field()
    job_desc = scrapy.Field()
    addr = scrapy.Field()
    gmt_create = scrapy.Field()
    gmt_update = scrapy.Field()

    def get_insert_sql(self):
        sql = '''
        insert into lagou_position(job_name,url,company,salary,city,experience,degree,job_catagory,tags,publish_date,job_desc,addr,gmt_create,gmt_update)
        values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        data = (
            self.get('job_name'),
            self.get('url'),
            self.get('company'),
            self.get('salary'),
            self.get('city'),
            self.get('experience'),
            self.get('degree'),
            self.get('job_catagory'),
            self.get('tags'),
            self.get('publish_date'),
            self.get('job_desc'),
            self.get('addr'),
            self.get('gmt_create'),
            self.get('gmt_update'),
        )
        return sql,data


class QccComanyItemLoader(ItemLoader):

    default_output_processor = TakeFirst()

class QccCompanyItem(scrapy.Item):
    name = scrapy.Field()
    leader = scrapy.Field()
    registry_capital = scrapy.Field()
    registry_date = scrapy.Field()
    phone = scrapy.Field()
    addr = scrapy.Field()




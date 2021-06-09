# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import datetime

import itemloaders.processors
import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, Join,Compose,MapCompose
from jobbole.utils.common import date_from_datetimestr,join

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
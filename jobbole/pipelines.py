# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
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
        from scrapy.pipelines.media import MediaPipeline
        print(results,item,info.__dict__)
        return item

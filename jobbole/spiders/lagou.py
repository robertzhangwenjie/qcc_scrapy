import datetime
import logging
import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jobbole.items import LagouPositionItem,LagouPositionItemLoader


class LagouSpider(CrawlSpider):
    name = 'lagou'
    allowed_domains = ['www.lagou.com']
    start_urls = ['https://www.lagou.com']

    custom_settings = {
        "COOKIES_ENABLED": False, #使用settings中的cookie
        'DEFAULT_REQUEST_HEADERS': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': 'JSESSIONID=ABAAABAABAGABFA9902336AAAA3A0799ABEA0D98FE68378; WEBTJ-ID=2021069%E4%B8%8B%E5%8D%884:37:26163726-179efeb4fcf34f-092a8f8e47c4f6-f7f1939-1327104-179efeb4fd0a04; RECOMMEND_TIP=true; user_trace_token=20210609163727-3e04db0d-f0e8-4e1f-b835-301e07bac54b; LGUID=20210609163727-f95ea327-cca7-46c9-85fc-d1d78882ca58; sensorsdata2015session=%7B%7D; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1623227847; _ga=GA1.2.1910619003.1623227847; index_location_city=%E5%85%A8%E5%9B%BD; __lg_stoken__=62f528591e7fb4de84111e055b3ea1c4fc1459d195d2d5113ccff9031d37ad6d999c82b2d6a74a0ad1ea0b84e923574122470971e39bd7e5babce84a4661cfab3150ff7c8e87; X_MIDDLE_TOKEN=06502de73e7464ecfb54812f730812bf; privacyPolicyPopup=false; _gid=GA1.2.785907713.1623316335; SEARCH_ID=7f5359b0f6cf480a95cde934ad37c070; TG-TRACK-CODE=jobs_similar; LGSID=20210611065922-c7239829-7ee7-4d70-862c-92f1e7b69cea; PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F; PRE_LAND=https%3A%2F%2Fwww.lagou.com%2Fzhaopin%2F; _gat=1; gate_login_token=7b875a97a171a16c5ed4aacd417cd7740dccd6bcde5ecc6c; LG_LOGIN_USER_ID=0f37d651c2be432b7b51240cdb3bb27b9c06a5a466cf9d14; LG_HAS_LOGIN=1; _putrc=0B1EDA8C9694BD43; login=true; unick=%E5%BC%A0%E6%96%87%E6%9D%B0; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=302; __SAFETY_CLOSE_TIME__9802620=1; X_HTTP_TOKEN=b86e41abaa3ac8d450166332610a0a7d51363dcdf9; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%229802620%22%2C%22first_id%22%3A%22179efeb5163b18-05e019f862daa1-f7f1939-1327104-179efeb5164c9c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24os%22%3A%22Windows%22%2C%22%24browser%22%3A%22Chrome%22%2C%22%24browser_version%22%3A%2291.0.4472.77%22%2C%22lagou_company_id%22%3A%22%22%7D%2C%22%24device_id%22%3A%22179efeb5163b18-05e019f862daa1-f7f1939-1327104-179efeb5164c9c%22%7D; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1623366105; LGRID=20210611070145-80e395d5-2056-4298-ac8f-69a6a863383a',
            'Host': 'www.lagou.com',
            'Referer': 'https://www.lagou.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        }
    }

    rules = (
        Rule(LinkExtractor(allow=(r'/zhaopin/',)),follow=True),
        Rule(LinkExtractor(allow=(r'/gongsi/v1/j/',r'/gongsi/v1/x/')),follow=True),
        Rule(LinkExtractor(allow=(r'/jobs/\d+.html',)), callback='parse_job', follow=True),
    )


    def parse_job(self, response):
        '''
        解析拉勾网的position
        :param response:
        :return:
        '''

        position_loader = LagouPositionItemLoader(item=LagouPositionItem(),response=response)
        position_loader.add_xpath('job_name','//div[@class="job-name"]/@title')
        position_loader.add_value('url',response.url)
        position_loader.add_xpath('company','//dd[@class="job_request"]//span[@class="company"]/text()')
        position_loader.add_xpath('salary','//span[@class="salary"]/text()')
        position_loader.add_xpath('city','//dd[@class="job_request"]/h3//span[1]/text()',re='(.*) \/')
        position_loader.add_xpath('experience','//dd[@class="job_request"]/h3//span[2]/text()',re='(.*) \/')
        position_loader.add_xpath('degree','//dd[@class="job_request"]/h3//span[3]/text()',re='(.*) \/')
        position_loader.add_xpath('job_catagory','//dd[@class="job_request"]/h3//span[4]/text()')
        position_loader.add_xpath('tags','//dd[@class="job_request"]//ul[@class="position-label clearfix"]//li/text()')

        _publish_date = response.xpath('//p[@class="publish_time"]').xpath('string(.)').get().strip().split('\n')[-1]
        publish_date = re.search(r'(.*)\xa0', _publish_date).group(1).strip()
        position_loader.add_value('publish_date',publish_date)
        position_loader.add_xpath('job_desc','//div[@class="job-detail"]')

        addr=response.xpath('//dd/div[@class="work_addr"]').xpath('string()').get().replace("\n","").replace(" ","").replace("查看地图","")

        position_loader.add_value('addr',addr)
        position_loader.add_value('gmt_create',datetime.datetime.now())
        position_loader.add_value('gmt_update',datetime.datetime.now())
        item =  position_loader.load_item()
        yield item
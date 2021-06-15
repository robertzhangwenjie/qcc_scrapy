import logging

import scrapy

from jobbole.items import QccComanyItemLoader,QccCompanyItem
from jobbole.qcc import cookie
from jobbole.qcc.company import Company


class QccSpider(scrapy.Spider):
    name = 'qcc'
    allowed_domains = ['www.qcc.com']
    search_url = 'https://www.qcc.com/web/search?key='


    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': {
            'Connection': 'keep-alive',
            'Host': 'www.qcc.com',
        }
    }


    def start_requests(self):
        # cookies= cookie.get_cookie(phone = '13995553697',password = 'zhangwenjie64656')
        company_list = Company.new_compay().get_newest_excel_company()

        for comany in company_list:
            url = self.search_url + comany
            yield scrapy.Request(url)

    def parse(self, response,**kwargs):
        item_loader = QccComanyItemLoader(QccCompanyItem(),response)

        try:
            company_name = response.xpath('//div[@class="maininfo"]/a[@class="title"]')[0].xpath('string()').get()
            item_loader.add_value('name', company_name)
        except IndexError as err:
            self.log('账号失效',logging.ERROR)



        relate_info = response.xpath('//div[@class="maininfo"]/div[@class="relate-info"]')[0]
        leader = relate_info.xpath('div[@class="rline"]/span[@class="f"]/span[@class="val"]').xpath('string()')[0].get()
        registry_capital = relate_info.xpath('div[@class="rline"]/span[@class="f"]/span[@class="val"]').xpath('string()')[1].get()
        registry_date = relate_info.xpath('div[@class="rline"]/span[@class="f"]/span[@class="val"]').xpath('string()')[2].get()
        phone = relate_info.xpath('div[@class="rline"]/span[@class="f"]/span[@class="val"]').xpath('string()')[3].get()
        addr = relate_info.css('span.val.long-text::text').get()

        item_loader.add_value('leader',leader)
        item_loader.add_value('registry_capital',registry_capital)
        item_loader.add_value('phone',phone)
        item_loader.add_value('registry_date',registry_date)
        item_loader.add_value('addr',addr)
        item = item_loader.load_item()
        yield item


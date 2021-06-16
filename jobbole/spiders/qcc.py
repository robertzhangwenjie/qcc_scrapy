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
            yield scrapy.Request(url,callback=self.parse_company_url)


    def parse_company_url(self,response):
        company_url = response.css('div.maininfo > a.title::attr(href)').get()
        yield scrapy.Request(company_url,callback=self.parse_detail)

    def parse_detail(self, response):

        item_loader = QccComanyItemLoader(QccCompanyItem(),response)

        company_name = response.css('#company-top div.row.title.jk-tip > h1::text').get()
        leader = response.css('div.dcontent span.text-primary span.text-primary')[0].xpath('string()').get()
        registry_capital = response.css('#Cominfo table.ntable  tr:nth-child(3) td:nth-child(2)::text').get()
        registry_date = response.css('#Cominfo table.ntable  tr:nth-child(2) td:last-child::text').get()
        phone = response.css('div.row span.phone-status + span::text').get()
        addr = response.css('div.dcontent > div.row:nth-child(3) > span.cvlu a:nth-child(1)::attr(title)').get()
        industry = response.css('#Cominfo table.ntable  tr:nth-child(6) td:nth-child(2)::text').get()
        scope = response.css('#Cominfo table.ntable  tr:last-child td:nth-child(2)::text').get()
        ip_sb = response.css('div.company-nav div.company-nav-tab:nth-child(6) div.company-nav-items span:nth-child(1)::text')[0].get().strip()
        ip_zl = response.css('div.company-nav div.company-nav-tab:nth-child(6) div.company-nav-items span:nth-child(1)::text')[2].get().strip()
        ip_rz = response.css('div.company-nav div.company-nav-tab:nth-child(6) div.company-nav-items span:nth-child(1)::text')[5].get().strip()
        ip = f"商标信息:{ip_sb},专利信息:{ip_zl},软件著作:{ip_rz}"

        item_loader.add_value('name', company_name)
        item_loader.add_value('leader',leader)
        item_loader.add_value('registry_capital',registry_capital)
        item_loader.add_value('phone',phone)
        item_loader.add_value('registry_date',registry_date)
        item_loader.add_value('addr',addr)
        item_loader.add_value('industry',industry)
        item_loader.add_value('scope',scope)
        item_loader.add_value('ip',ip)
        item = item_loader.load_item()
        yield item




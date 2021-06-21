import logging
import re

import scrapy

from jobbole import settings
from jobbole.items import QccComanyItemLoader,QccCompanyItem
from jobbole.qcc.company_excel import CompanyExcelHandler
from jobbole.qcc.cookie import MysqlConnector,QccCookie



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

        # 初始化企查查的cookie
        QccCookie().init_cookies()
        # 获取excel目录下所有excel的企业名称
        company_list = CompanyExcelHandler(excel_dir_pah=settings.COMPANY_EXCEL_PATH_DIR).get_company_names()

        company_cralwed = self.get_crawled_company()
        for company in company_list:
            if company not in company_cralwed:
                url = self.search_url + company
                yield scrapy.Request(url,callback=self.parse_company_url)

    def get_crawled_company(self):

        company_list = []
        mysql = MysqlConnector()
        query = '''
        select name from qcc_company
        '''
        mysql.cursor.execute(query)
        company_tuples = mysql.cursor.fetchall()
        for company_tuple in company_tuples:
            company_list.append(company_tuple[0])
        return company_list


    def parse_company_url(self,response):
        company_url = response.css('div.maininfo > a.title::attr(href)').get()
        yield scrapy.Request(company_url,callback=self.parse_detail)

    def parse_detail(self, response):


        # company_name = response.css('#company-top div.row.title.jk-tip > h1::text').get()
        company_name = response.css('div.company-header  div.title > h1::text').get()
        leader = response.css('span.max-150').xpath('string()').get()

        registry_capital = response.css('#cominfo table.ntable  tr:nth-child(3) td:nth-child(2)::text').get()
        registry_date = response.css('#cominfo table.ntable  tr:nth-child(2) td:last-child::text').get()
        phone = response.css('span.phone-status + span::text').get()
        addr = response.css('#cominfo table.ntable  tr:nth-child(9) td:nth-child(2) > a.text-dk::text').get()
        industry = response.css('#cominfo table.ntable  tr:nth-child(6) td:nth-child(2)::text').get().strip()
        scope = response.css('#cominfo table.ntable > tr:last-child > td:nth-child(2)::text').get()

        company_base_info = {
            "name": company_name,
            "registry_capital": registry_capital,
            "leader": leader,
            "registry_date": registry_date,
            "phone": phone,
            "addr": addr,
            "industry": industry,
            "scope": scope
        }
        cassets_url = 'https://www.qcc.com/cassets/' + re.search(r'.*/(.*)\.html$',response.url).group(1) + '.html'
        yield response.follow(cassets_url,meta={"company_base_info":company_base_info},callback=self.parse_cassets,dont_filter=True)

    def parse_cassets(self,response):
        item_loader = QccComanyItemLoader(QccCompanyItem(),response)

        ip_sb = response.css('div.data-assets > div.sub-nav > a.item:nth-child(1)::text').get().strip()
        ip_zl = response.css('div.data-assets > div.sub-nav > a.item:nth-child(2)::text').get().strip()
        ip_rz = response.css('div.data-assets > div.sub-nav > a.item:nth-child(5)::text').get().strip()
        ip = f"{ip_sb},{ip_zl},{ip_rz}"


        company_base_info = response.meta['company_base_info']
        item_loader.add_value('name', company_base_info['name'])
        item_loader.add_value('leader',company_base_info['leader'])
        item_loader.add_value('registry_capital',company_base_info['registry_capital'])
        item_loader.add_value('phone',company_base_info['phone'])
        item_loader.add_value('registry_date',company_base_info['registry_date'])
        item_loader.add_value('addr',company_base_info['addr'])
        item_loader.add_value('industry',company_base_info['industry'])
        item_loader.add_value('scope',company_base_info['scope'])
        item_loader.add_value('ip',ip)
        item = item_loader.load_item()
        yield item




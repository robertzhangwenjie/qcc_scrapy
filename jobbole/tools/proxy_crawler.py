from urllib.parse import urljoin

import fake_useragent
import requests
from scrapy import Selector
import pymysql
from jobbole import settings


class Proxy66IPCrawler:

    start_url = 'http://www.66ip.cn/'

    def __init__(self, max_page_size=70,base_url=None):
        self.headers = {
            'User-Agent': fake_useragent.UserAgent().random
        }
        self.proxy_addrs = set()
        self.current_page = 1
        self.max_page_size = max_page_size
        self.base_url = base_url or self.start_url

        self.conn = pymysql.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DB, user=settings.MYSQL_USER,
                               password=settings.MYSQL_PASSWORD)
        self.cursor = self.conn.cursor()

    def start_requests(self):
        '''
        crawl proxy ip in 66ip website
        :return:
        '''
        res = self._get_response(self.base_url)
        amount = res.xpath('//div[@align="center"]//p[@class="style7"]/span//text()').get()
        print(f"ip代理总数：{amount}")
        self.parse_url(res)


    def parse_url(self,response):
        proxy_info_list = response.xpath('//div[@align="center"]/table//tr[position()>1]')
        for proxy in proxy_info_list:
            if proxy_addr := self._get_proxy_addr(proxy):
                print(proxy_addr)
                self.proxy_addrs.add(proxy_addr)
        _next_page = response.xpath('//div[@id="PageList"]/a[last()]')
        next_page_class = _next_page.xpath('@class').get()

        next_page_url = _next_page.xpath('@href').get()
        if next_page_class != "pageCurrent":
            self.current_page += 1
            if self.current_page > self.max_page_size:
                print(f'已爬取{len(self.proxy_addrs)}个代理ip')
                self._insert_mysql()
                return
            res = self._get_response(urljoin(self.base_url, next_page_url))
            self.parse_url(res)
        else:
            print(f'已爬取{len(self.proxy_addrs)}个代理ip')

    def _get_response(self,url):
        res = requests.get(url, headers=self.headers)
        res.encoding = res.apparent_encoding
        response = Selector(text=res.text)
        return response


    def _get_proxy_addr(self, proxy):
        try:
            ip = proxy.css('td::text').extract()[0]
            port = proxy.css('td::text').extract()[1]

            proxy_addr = f'http://{ip}:{port}'
            return proxy_addr
        except Exception as err:
            print(err)
            return None

    def _insert_mysql(self):

        query = '''
        insert into proxy_ip(proxy_addr) values (%s) 
        on duplicate key update proxy_addr = values(proxy_addr)
        '''
        self.cursor.executemany(query,self.proxy_addrs)
        self.conn.commit()
        self.conn.close()


if __name__ == '__main__':
    crawler = Proxy66IPCrawler()
    crawler.start_requests()

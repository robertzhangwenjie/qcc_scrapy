import pymysql
import requests

from jobbole import settings


class ProxyUtil:

    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DB, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD)
        self.cursor = self.conn.cursor()

    @staticmethod
    def is_proxy_available(proxy):
        proxy_dict = {
            'http': proxy
        }
        try:
            res = requests.get('https://www.baidu.com', proxies=proxy_dict)
            if res.status_code == 200:
                return True
        except Exception as err:
            print("invalid proxy")
        return False

    def delete_proxy(self, proxy):
        query = '''
            delete from proxy_ip where proxy_addr = proxy
            '''
        self.cursor.execute(query)
        self.conn.commit()

    def get_random_proxy(self):

        query = '''
            select proxy_addr from proxy_ip as t1 
                join (select round(rand() * ((select max(id) from proxy_ip) - (select min(id) from proxy_ip)) + (select min(id) from proxy_ip)) as id) as t2
                on t1.id >= t2.id limit 1
            '''
        self.cursor.execute(query)
        proxy = self.cursor.fetchone()[0]
        if not self.is_proxy_available(proxy):
            self.delete_proxy(proxy)
            return self.get_random_proxy()
        return proxy


if __name__ == '__main__':
    proxy = ProxyUtil()
    addr = proxy.get_random_proxy()
    print(proxy.is_proxy_available(addr))
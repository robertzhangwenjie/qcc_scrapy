import pymysql
import requests

from jobbole import settings


class ProxyUtil:

    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DB, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD)
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)

    @staticmethod
    def is_proxy_available(proxy):
        proxy_dict = {
            'http': f'{proxy[0]}:{proxy[1]}'
        }
        try:
            res = requests.get('https://www.baidu.com', proxies=proxy_dict,timeout=(2,4))
            if res.status_code == 200:
                print('valied proxy')
                return True
        except Exception as err:
            print("invalid proxy")
            return False

    def delete_proxy(self, proxy):
        query = '''
            delete from proxy where ip = %s and port = %s
            '''
        print(f'delete proxy: {proxy}')
        self.cursor.execute(query,proxy)

    def get_random_proxy(self):

        query = '''
            select ip,port from proxy as t1 
                join (select round(rand() * ((select max(id) from proxy) - (select min(id) from proxy)) + (select min(id) from proxy)) as id) as t2
                on t1.id >= t2.id limit 1
            '''
        self.cursor.execute(query)
        if proxy :=self.cursor.fetchone():
            return proxy



if __name__ == '__main__':
    proxy = ProxyUtil()
    addr = proxy.get_random_proxy()
    print(proxy.is_proxy_available(addr))
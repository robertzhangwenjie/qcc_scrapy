import pymysql
import requests
from fake_useragent import UserAgent

from jobbole import settings
from jobbole.qcc.qcc_selenium import QccSelenium

class MysqlConnector:
    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DB, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD)
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)

class QccCookie(MysqlConnector):

    def __init__(self):
        super().__init__()

    def delete_cookie(self,cookie:str):

        query = '''
        delete from qcc_cookies where cookie = %s
        '''
        if self.is_exist(cookie):
            self.cursor.execute(query,(cookie,))

    def clear_cookie(self):
        query = '''
        delete from qcc_cookies
        '''
        self.cursor.execute(query)

    def is_exist(self,cookie):
        query = '''
        select cookie from qcc_cookies where cookie = %s
        '''
        if self.cursor.execute(query,(cookie,)) == 0:
            return False
        return True

    def get_random_cookie(self):
        '''
        获取cookie，如果cookie失效则删除，如果获取不到则使用selenium模拟登录获取cookie
        :return:
        '''
        query = '''
        select cookie from qcc_cookies order by rand() limit 1
        '''
        if self.cursor.execute(query) == 0:
            print("no cookie available,starting get cookie by qcc selenium")
            self.init_cookies()
            return self.get_random_cookie()

        cookie = self.cursor.fetchone()[0]
        verify_url = 'https://www.qcc.com/user_home'
        if self.verify_cookie(verify_url,cookie):
            return cookie
        else:
            self.delete_cookie(cookie)
            return self.get_random_cookie()

    def put_cookie(self,phone,cookie):
        if isinstance(cookie,list):
            cookie = str_cookie_from_list(cookie)
        query = '''
        insert into qcc_cookies(phone,cookie) values(%s,%s) 
        '''
        if self.is_exist(cookie):
            return
        self.cursor.execute(query,(phone,cookie))

    @staticmethod
    def dict_cookie_from_str(cookies: str):
        cookie_list = cookies.split(";")
        cookie_dict = {}
        for cookie in cookie_list:
            key,value = tuple(cookie.split("="))
            cookie_dict[key.strip()] = value.strip()
        return cookie_dict


    @staticmethod
    def verify_cookie(url,cookie: str):
        headers = {
            'User-Agent': UserAgent().random,
            'Host': 'www.qcc.com',
            'Cookie': cookie
        }
        res = requests.get(url,headers=headers,allow_redirects=False)
        if res.status_code == 200:
            return True
        else:
            return False

    def get_phone_by_cookie(self,cookie):
        query = '''
        select phone from qcc_cookies where cookie = %s
        '''
        if self.cursor.execute(query,(cookie,)):
            return self.cursor.fetchone()[0]
        else:
            raise ValueError('cookie is not found')

    def init_cookies(self):
        self.clear_cookie()
        for account in settings.QCC_ACCOUNTS:
            cookie_str = get_cookie_by_selenium(account['phone'], account['password'])
            self.put_cookie(account['phone'],cookie_str)

def get_cookie_by_selenium(phone, password) ->str:
    qs = QccSelenium()
    qs.login(phone, password)
    cookies_selenium = qs.get_cookies()
    cookie_str = str_cookie_from_list(cookies_selenium)
    qs.exit()
    return cookie_str

def str_cookie_from_dict(cookies: dict) ->str:
    cookies_list = []
    for key,value in cookies.items():
        item = f'{key}={value}'
        cookies_list.append(item)
    return ";".join(cookies_list)

def str_cookie_from_list(cookies: list) ->str:

    cookie_list = []
    try:
        for cookie in cookies:
            cookie_list.append(f"{cookie['name']}={cookie['value']}")
    except Exception as err:
        raise ValueError('cookies must be list[dict]')
    return ";".join(cookie_list)

if __name__ == '__main__':
    pass
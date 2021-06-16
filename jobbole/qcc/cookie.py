import time

import pymysql
import requests
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.common.by import By

from jobbole import settings
from jobbole.utils import common

class QccSelenium:

    phone_input = By.ID, 'nameNormal' # 手机输入框
    password_input = By.ID, 'pwdNormal' # 密码输入框
    verify_scroll_btn = By.ID, 'nc_2_n1z' # 验证滑块
    scroll_success_btn = By.CSS_SELECTOR, 'div#nc_2__scale_text > span.nc-lang-cnt' # 滑动成功按钮
    login_btn = By.CSS_SELECTOR, 'form#user_login_normal button[type="submit"]' # 登录按钮
    refresh_btn = By.PARTIAL_LINK_TEXT,'刷新' # 滑动失败时的刷新按钮

    def __init__(self,base_url = 'https://www.qcc.com/'):
        self.base_url = base_url

        driver_option = webdriver.ChromeOptions()
        # 企查查会根据浏览器的window.navigator.webdriver来判断是否是爬虫，需要手动设置为False，方式反爬虫检测
        driver_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver_option.add_argument("--no-sandbox")
        driver_option.add_argument("--disable-dev-usage")

        self.driver = webdriver.Chrome(executable_path=settings.ChromeDriver,options=driver_option)
        self.driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument",{
            "source": '''
                Object.defineProperty(navigator,'webdriver',{
                    get: () => undefined
                })
            '''
        })
        self.driver.implicitly_wait(5)



    def login(self,username,password):
        self.driver.get(self.base_url)

        # 点击登录
        self.driver.find_element(By.PARTIAL_LINK_TEXT,'登录').click()
        # 选择密码登录
        self.driver.find_element(By.PARTIAL_LINK_TEXT,'密码登录').click()
        # 输入手机号和密码
        self.driver.find_element(*self.phone_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        # 滑动验证码
        self._scroll_btn_verify(308)
        # 登录
        self.driver.find_element(*self.login_btn).click()

        # 判断是否登录成功
        login_failed_ele = By.CSS_SELECTOR,'label#nameNormal-error'
        if common.is_element_exist(self.driver,login_failed_ele):
            print("登录失败")
            self.driver.close()
            return False
        else:
            print('登录成功')
            return True

    def logout(self):
        self.driver.get(f'{self.base_url}/user_logout')

    def exit(self):
        self.driver.close()

    def _scroll_btn_verify(self, offset, retry_num=5):
        '''
        滑动验证码进行验证
        :param offset: 滑动的距离
        :param retry_num: 重试的次数
        :return:
        '''
        scroll_times = 0
        while True:
            # 滑动
            common.scroll_btn(self.driver,self.verify_scroll_btn,offset)
            # 查看是否滑动成功
            if common.is_element_exist(self.driver, self.scroll_success_btn):
                print('滑动验证成功')
                return

            # 点击刷新重新滑动
            self.driver.find_element(*self.refresh_btn).click()
            scroll_times += 1
            if scroll_times >= retry_num:
                print(f'滑动失败超过{scroll_times}次，登录失败')
                self.driver.close()

    def get_cookies(self):
        cookies = self.driver.get_cookies()
        return cookies


class QccCookie:

    def __init__(self):
        self.conn = pymysql.connect(host=settings.MYSQL_HOST, db=settings.MYSQL_DB, user=settings.MYSQL_USER,
                                    password=settings.MYSQL_PASSWORD)
        self.cursor = self.conn.cursor()
        self.conn.autocommit(True)

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

    def get_cookie(self):
        '''
        获取cookie，如果cookie失效则删除，如果获取不到则使用selenium模拟登录获取cookie
        :return:
        '''
        query = '''
        select cookie from qcc_cookies order by rand() limit 1
        '''
        if self.cursor.execute(query) == 0:
            print("no cookie available,starting get cookie by qcc selenium")
            cookie = get_cookie_str(settings.QCC_ACCOUNT['username'],settings.QCC_ACCOUNT['password'])
            self.put_cookie(cookie)
            return cookie

        cookie = self.cursor.fetchone()[0]
        verify_url = 'https://www.qcc.com/user_home'
        if self.verify_cookie(verify_url,cookie):
            return cookie
        else:
            self.delete_cookie(cookie)
            self.get_cookie()

    def put_cookie(self,cookie):
        if isinstance(cookie,list):
            cookie = str_cookie_from_selenium(cookie)
        query = '''
        insert into qcc_cookies(cookie) values(%s) 
        '''
        if self.is_exist(cookie):
            return
        self.cursor.execute(query,(cookie,))

    @staticmethod
    def dict_cookie_from_str(cookies: str):
        cookie_list = cookies.split(";")
        cookie_dict = {}
        for cookie in cookie_list:
            key,value = tuple(cookie.split("="))
            cookie_dict[key.strip()] = value.strip()
        return cookie_dict


    def get_cookie_dict(self):
        cookie_str = self.get_cookie()
        return self.dict_cookie_from_str(cookie_str)

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

def get_cookie_str(phone,password):
    qs = QccSelenium()
    qs.login(phone, password)
    cookies_selenium = qs.get_cookies()
    cookies_str = str_cookie_from_selenium(cookies_selenium)
    qs.exit()
    return cookies_str

def str_cookie_from_dict(cookies: dict):
    cookies_list = []
    for key,value in cookies.items():
        item = f'{key}={value}'
        cookies_list.append(item)
    return ";".join(cookies_list)

def str_cookie_from_selenium(cookies: list):

    cookie_list = []
    try:
        for cookie in cookies:
            cookie_list.append(f"{cookie['name']}={cookie['value']}")
    except Exception as err:
        raise ValueError('cookies must be list[dict]')
    return ";".join(cookie_list)

if __name__ == '__main__':
    q = QccSelenium()
    q.login('13995553697','zhangwenjie64656')
    cookies = q.get_cookies()
    cookie_str = str_cookie_from_selenium(cookies)
    print(cookie_str)
    q.exit()
    QccCookie().clear_cookie()
    QccCookie().put_cookie(cookie_str)
    # url = 'https://www.qcc.com/web/search?key=' + '深圳弘文科技'
    # headers = {
    #     'User-Agent': UserAgent().random,
    #     'Connection': 'keep-alive',
    #     'Host': 'www.qcc.com',
    #     'Cookie': str_cookie_from_selenium(cookies)
    # }
    # res = requests.get(url,headers=headers)
    # res.encoding = res.apparent_encoding
    # print(res.text)

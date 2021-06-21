import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from jobbole import settings
from jobbole.utils import common


class QccSelenium:

    login_or_registry= By.PARTIAL_LINK_TEXT,'登录' # 登录注册按钮
    passwd_login_btn = By.PARTIAL_LINK_TEXT,'密码登录' # 密码登录选择按钮

    phone_input = By.ID, 'nameNormal' # 手机输入框
    password_input = By.ID, 'pwdNormal' # 密码输入框
    verify_scroll_btn = By.ID, 'nc_2_n1z' # 验证滑块
    scroll_success_btn = By.CSS_SELECTOR, 'div#nc_2__scale_text > span.nc-lang-cnt' # 滑动成功按钮
    login_btn = By.CSS_SELECTOR, 'form#user_login_normal button[type="submit"]' # 登录按钮
    refresh_btn = By.PARTIAL_LINK_TEXT,'刷新' # 滑动失败时的刷新按钮

    login_failed_ele = By.CSS_SELECTOR, 'label#nameNormal-error' # 登录失败时的元素
    # 滑块移动的距离
    move_offset = 308

    def __init__(self,base_url = 'https://www.qcc.com/'):
        self.base_url = base_url

        driver_option = webdriver.ChromeOptions()
        # 企查查会根据浏览器的window.navigator.webdriver来判断是否是爬虫，需要手动设置为False，方式反爬虫检测
        driver_option.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver_option.add_argument("--no-sandbox")
        driver_option.add_argument("--disable-dev-usage")
        prefs = {"profile.managed_default_content_settings.images": 2}
        driver_option.add_experimental_option("prefs",prefs)

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

        # 点击登录注册
        self.driver.find_element(*self.login_or_registry).click()
        # 选择密码登录
        self.driver.find_element(*self.passwd_login_btn).click()
        # 输入手机号和密码
        self.driver.find_element(*self.phone_input).send_keys(username)
        self.driver.find_element(*self.password_input).send_keys(password)
        # 滑动验证码
        self._scroll_btn_verify(self.move_offset)
        # 登录
        self.driver.find_element(*self.login_btn).click()

        # 判断是否登录成功
        if common.is_element_exist(self.driver,self.login_failed_ele):
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
            time.sleep(1)
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

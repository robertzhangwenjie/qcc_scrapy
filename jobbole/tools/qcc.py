import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from jobbole.utils import common


class QichachaLoginPage:
    '''
    企查查登录页面
    '''

    def __init__(self):
        self.login_link = By.LINK_TEXT,'登录'
        self.login_with_password = By.ID,'normalLogin'
        # 手机输入框
        self.phone_input = By.ID,'nameNormal'
        # 密码输入框
        self.password_input = By.ID,'pwdNormal'

        # 登录页面
        # 登录滑块
        self.verify_scroll_btn = By.ID, 'nc_1_n1z'

        # 登录框按钮定位
        self.refresh_scroll = By.LINK_TEXT,'刷新'
        self.login_btn = By.CSS_SELECTOR,'#user_login_normal > button[type="submit"]'

        #验证码框
        self.verification_code_input = By.ID,'nc_1_captcha_input'
        self.submit_btn = By.ID,'nc_1_scale_submit'
        self.refresh_btn = By.ID,'nc_1__btn_1'
        # 错误信息提示
        self.error_span = By.CSS_SELECTOR,'#nc_1__captcha_img_text > span'

        # 验证码错误次数
        self.max_error_times = 3



    def _scroll(self,driver,offset):
        '''
        拖动滑块
        :param driver:
        :param offset: 拖动的距离
        :return:
        '''
        button = driver.find_element(*self.verify_scroll_btn)
        action = ActionChains(driver)
        action.click_and_hold(button).perform()
        action.reset_actions()
        action.move_by_offset(offset, 0).perform()

    def scroll_btn_move(self,driver,offset=308):
        scroll_times = 0
        while True:
            # 滑动
            self._scroll(driver,offset)
            # 查看是否滑动成功
            refresh_btn = common.is_element_exist(driver,self.refresh_scroll)
            if not refresh_btn:
                break
            # 点击刷新重新滑动
            time.sleep(2)
            refresh_btn.click()
            scroll_times +=1
            if scroll_times >=5:
                print(f'滑动失败超过{scroll_times}次')
                flag = input('请手动滑动后，输入Y确定:')
                if flag in ('Y','y'):
                    break
                print(f'手动滑动失败')
    def input_verification_code(self,driver):
        error_times = 0
        while True:
            driver.find_element(*self.verification_code_input).clear()
            verification_code = input('请输入验证码:')
            if verification_code in ('y','Y'):
                break
            driver.find_element(*self.verification_code_input).send_keys(verification_code)
            driver.find_element(*self.submit_btn).click()
            if not common.is_element_exist(driver,self.error_span):
                break
            error_times +=1
            if error_times >= self.max_error_times:
                raise ValueError('验证码输入错误次数超过3次')


if __name__ == '__main__':
    pass
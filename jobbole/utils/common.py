import datetime
import hashlib
import typing

from itemloaders.processors import Join
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains


def get_md5(value: typing.Union[str,bytes]):
    if isinstance(value,str):
        # 如果是str，则转换为bytes对象
        value = value.encode()
    if not isinstance(value,(bytes, bytearray, memoryview)):
        raise TypeError('value must be bytes or str')
    md5 = hashlib.md5()
    # 往md5对象中添加需要转换的bytes
    md5.update(value)
    return md5.hexdigest()

def date_from_datetimestr(value):
    return datetime.datetime.strptime(value,"%Y-%m-%d %H:%M:%S").date()


# 判断元素是否存在,存在就返回该元素
def is_element_exist(driver,element):
    try:
        ret = driver.find_element(*element)
    except (NoSuchElementException) as err:
        return False
    if ret:
        return ret
    return False

# 判断元素是否可见
def is_element_display(driver,element):
    try:
        ret = driver.find_element(*element)
    except (NoSuchElementException) as err:
        return False
    if ret.is_displayed():
        return True
    return False


def scroll_btn(driver,btn_selector,offset):
    '''
    拖动滑块验证
    :param driver:
    :param offset: 拖动的距离
    :return:
    '''
    button = driver.find_element(*btn_selector)
    action = ActionChains(driver)
    action.click_and_hold(button).perform()
    action.reset_actions()
    action.move_by_offset(offset, 0).perform()





if __name__ == '__main__':
    pass
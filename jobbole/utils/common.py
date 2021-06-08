import datetime
import hashlib
import typing

from itemloaders.processors import Join


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

def join(value):
    res = Join(",")(value)
    if res:
        return res
    else:
        return ""
if __name__ == '__main__':
    pass
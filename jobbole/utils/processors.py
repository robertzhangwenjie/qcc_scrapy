# define the processors for itemloaders


class CustomTakeFirst:
    '''
    自定义TakeFirst类，当值为空list时，返回空字符串
    '''
    def __call__(self, values):
        if values == []:
            return ""
        for value in values:
            if value is not None and value != '':
                return value


if __name__ == '__main__':
    pass
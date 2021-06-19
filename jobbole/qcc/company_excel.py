#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/6/1 7:54
# @Author   :   robert
# @FileName :   company_source.py
# @Software :   PyCharm
import os

from jobbole.utils.excel_handler import ExcelHandler
from abc import ABC, abstractmethod
from jobbole import settings


class CompanyExcelHandler:
    '''
        获取excel中需要爬取的企业基本信息
    '''
    def __init__(self, excel_dir_pah):
        self.company_exec_dir = excel_dir_pah

    def get_company_excels(self):
        # 获取目录下所有的文件
        file_list = os.listdir(self.company_exec_dir)
        # 初始化一个存放excel的列表
        _company_excel_list = []
        # 对文件进行排序，并去除非excel文件
        for file in file_list:
            if file.endswith('xls') or file.endswith('xlsx'):
                _company_excel_list.append(file)
        # 按照文件修改时间进行排序
        _company_excel_list.sort(key=lambda fn: os.path.getmtime(os.path.join(self.company_exec_dir, fn)),reverse=True)
        if len(_company_excel_list) == 0:
            raise ValueError('缺少公司信息表')
        # 返回最新修改或创建的excel

        company_excel_path_list = []

        for company_excel in _company_excel_list:
            excel_fullpath = os.path.join(self.company_exec_dir, company_excel)
            company_excel_path_list.append(excel_fullpath)
        return company_excel_path_list

    def get_company_names(self,sheet_id=0,num=-1):
        '''

        :param sheet_id: excel中的sheet的索引值
        :param num: 获取excel的数量，-1表示所有的excel都获取，1表示获取第一个(按照修改时间排序)
        :return:
        '''

        company_excel_list = self.get_company_excels()
        if num < 0:
            num = len(company_excel_list)
        company_names = []

        company_excel_list = company_excel_list[:num]

        for company_excel in company_excel_list:
            company_excel_handler = ExcelHandler(file_name=company_excel,sheet_index=0)
            # 获取要抓取的所有公司名称,获取第一列的值
            _company_names = company_excel_handler.get_col_values(0)
            # 去掉excel的第一行的"公司名称"
            _company_names.pop(0)
            company_names = company_names + _company_names
        # 去掉空企业
        res = filter(None, company_names)
        # 去掉重复企业
        res = set(res)
        return list(res)


if __name__ == '__main__':
    excel_handler = CompanyExcelHandler(excel_dir_pah=settings.COMPANY_EXCEL_PATH_DIR)
    print(excel_handler.get_company_excels())
    print(excel_handler.get_company_names())

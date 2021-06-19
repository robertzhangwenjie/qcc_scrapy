#!/usr/bin/python3
# -*- coding:utf-8 -*-
# @Time     :   2019/5/31 23:47
# @Author   :   robert
# @FileName :   excel_handler.py
# @Software :   PyCharm
import os
import datetime
import time

import xlrd
from xlrd import  xldate_as_datetime


class ExcelHandler(object):
    def __init__(self, file_name,sheet_index=0):
        self.file_name = file_name
        self._sheet = self._get_sheet_by_index(sheet_index)

    # 获取行数
    def nrows(self):
        return self._sheet.nrows

    # 获取sheet的内容
    def _get_sheet_by_index(self, sheet_index=0):
        if isinstance(sheet_index, int) and sheet_index >= 0:
            sheet_index = sheet_index
        else:
            raise ValueError("sheet_id must be integer")

        book = xlrd.open_workbook(self.file_name)
        sheet = book.sheet_by_index(sheet_index)
        return sheet

    # 获取第几列的值，col_index为列的索引值
    def get_col_values(self, col_index):
        col_values = []
        col_cells = self._sheet.col_slice(col_index)
        for cell in col_cells:
            col_values.append(self.get_cell_value(cell))
        return col_values


    def get_row_values(self,row_index):
        '''
        根据行的索引值获取指定行的所有数据
        :param row_index:
        :return: 指定行的值
        '''
        row_values = []
        col_cells = self._sheet.row(row_index)
        for cell in col_cells:
            row_values.append(self.get_cell_value(cell))
        return row_values

    @staticmethod
    def get_cell_value(cell):
        '''
        获取指定行、列的值
        :param row_index:
        :param col_index:
        :return:
        '''
        if cell.ctype == 2 and cell.value % 1 == 0:  # 如果是整形
            cell_value = int(cell.value)
        elif cell.ctype == 3: # 时间类型
            cell_value = xldate_as_datetime(cell.value,0)
        elif cell.ctype == 4: #bool类型
            cell_value = True if cell.value == 1 else False
        else:
            cell_value = cell.value
        return cell_value




if __name__ == '__main__':
    pass


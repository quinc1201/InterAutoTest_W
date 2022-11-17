#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import xlrd


# 目的：参数化，pytest list
# 自定义异常
class SheetTypeError:
    pass

# 1、验证文件是否存在，存在读取，不存在报错
class ExcelReader:
    def __init__(self, excel_file, sheet_by):
        if os.path.exists(excel_file):
            self.excel_file = excel_file
            self.sheet_by = sheet_by
            self._data = list()
        else:
            raise FileNotFoundError('文件不存在')

    # 2、读取sheet方式：名称，索引
    def data(self):
        # self._data存在不再读取，不存在则读取
        if not self._data:
            workbook = xlrd.open_workbook(self.excel_file)
            if type(self.sheet_by) not in [str, int]:
                raise SheetTypeError('请输入int or str')
            elif type(self.sheet_by) == int:
                sheet = workbook.sheet_by_index(self.sheet_by)
            elif type(self.sheet_by) == str:
                sheet = workbook.sheet_by_name(self.sheet_by)

            # 3、读取sheet内容
            # 返回格式：list，元素：字典
            # 获取首行信息
            title = sheet.row_values(0)
            # 遍历测试行，与首行组成dict，放在list中
            for row in range(1, sheet.nrows):
                row_value = sheet.row_values(row)
                row_dict = zip(title, row_value)
                self._data.append(dict(row_dict))
        # 4、结果返回
        return self._data


if __name__ == '__main__':
    data = ExcelReader('../data/testdata.xls', 0).data()
    print(data)
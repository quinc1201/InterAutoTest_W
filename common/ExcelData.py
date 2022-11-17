#!/usr/bin/python
# -*- coding: UTF-8 -*-
from utils.ExcelUtil import ExcelReader
from common.ExcelConfig import DataConfig


class Data:
    def __init__(self, testcase_file, sheet_by):
        # 1、使用excel工具类，获取结果list
        # self.reader = ExcelReader('../data/testdata.xls', 0)
        self.reader = ExcelReader(testcase_file, sheet_by)

    def get_run_list(self):
        """
        2、根据“是否运行”是否为y，获取执行用例列表
        :return:
        """
        run_list = list()
        for line in self.reader.data():
            if str(line[DataConfig().is_run]).lower() == 'y':
                # 3、保存要执行的测试用例，放到新的列表
                run_list.append(line)
        return run_list

    def get_case_list(self):
        """
        获取全部测试用例
        :return:
        """
        # case_list = list()
        # for line in self.reader.data():
        #         case_list.append(line)
        case_list = [line for line in self.reader.data()]
        return case_list

    def get_case_pre(self, pre):
        """
        根据前置条件，从全部测试用例中取到对应的测试用例
        :param pre:
        :return:
        """
        case_list = self.get_case_list()
        for line in case_list:
            if pre in dict(line).values():
                return line
        return None
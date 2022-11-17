#!/usr/bin/python
# -*- coding: UTF-8 -*-
from config.conf import ConfigYaml
from common.ExcelData import Data
import os
from utils.LogUtil import my_log
from common.ExcelData import DataConfig
from utils.RequestsUtil import Request
import json
import pytest
from common import Base
from utils.AssertUtil import AssertUtil
import allure
from config import conf


# 1、初始化信息
# 初始化测试用例文件
case_file = os.path.join('../data', ConfigYaml().get_excel_file())
# 初始化测试用例sheet名称
sheet_name = ConfigYaml().get_excel_sheet()
# 获取需要执行的测试用例列表
data_init = Data(case_file, sheet_name)
run_list = data_init.get_run_list()
# print(case_list)
# 日志
log = my_log()
# 初始化DataConfig
data_key = DataConfig()


# 2、测试用例方法，参数化运行
# 一个用例的执行
class TestExcel:
    def run_api(self, url, method, params=None, headers=None, cookies=None):
        """
        发送请求
        :param url:
        :param method:
        :param params:
        :param headers:
        :param cookies:
        :return:
        """
        # 接口请求
        request = Request()
        # params转换成json格式
        # 验证params是否为空
        if len(str(params).strip()) is not 0:
            params = json.loads(params)
        if str(method).lower() == 'get':
            res = request.get(url, json=params, headers=headers, cookies=cookies)
        elif str(method).lower() == 'post':
            res = request.post(url, json=params, headers=headers, cookies=cookies)
        else:
            res = None
            log.error('请求方式{}错误'.format(method))
        return res

    def run_pre(self, pre_case):
        url = ConfigYaml().get_conf_url() + pre_case[data_key.url]
        method = pre_case[data_key.method]
        params = pre_case[data_key.params]
        headers = pre_case[data_key.headers]
        cookies = pre_case[data_key.cookies]
        # 判断headers是否存在，json转义
        # # 增加cookies
        headers = Base.json_parse(headers)
        cookies = Base.json_parse(cookies)
        res = self.run_api(url, method, params, headers, cookies)
        print('前置用例执行：{}'.format(res))
        return res

    # 初始化信息：url, data
    @pytest.mark.parametrize('case', run_list)
    def test_run(self, case):
        # data_key = DataConfig()
        # 根据key获取case_list元素中dict的value
        url = ConfigYaml().get_conf_url() + case[data_key.url]
        case_id = case[data_key.case_id]
        case_moduel = case[data_key.case_moduel]
        case_name = case[data_key.case_name]
        pre_exec = case[data_key.pre_exec]
        method = case[data_key.method]
        params_type = case[data_key.params_type]
        params = case[data_key.params]
        expect_result = case[data_key.expect_result]
        actual_result = case[data_key.actual_result]
        is_run = case[data_key.is_run]
        headers = case[data_key.headers]
        cookies = case[data_key.cookies]
        code = case[data_key.code]
        db_verify = case[data_key.db_verify]
        # print('db_verify：{}'.format(db_verify))

        # 验证前置条件是否存在
        if pre_exec:
            # 获取有前置条件的测试用例
            pre_case = data_init.get_case_pre(pre_exec)
            # print(pre_case)
            pre_res = self.run_pre(pre_case)
            headers, cookies = self.get_correlation(headers, cookies, pre_res)

        # 判断headers是否存在，json转义
        # if headers:
        #     headers = json.loads(headers)
        # # 增加cookies
        # if cookies:
        #     cookies = json.loads(cookies)
        headers = Base.json_parse(headers)
        cookies = Base.json_parse(cookies)
            
        # 接口请求
        # request = Request()
        # # params转换成json格式
        # # 验证params是否为空
        # if len(str(params).strip()) is not 0:
        #     params = json.loads(params)
        # if str(method).lower() == 'get':
        #     res = request.get(url, json=params, headers=headers, cookies=cookies)
        # elif str(method).lower() == 'post':
        #     res = request.post(url, json=params, headers=headers, cookies=cookies)
        # else:
        #     log.error('请求方式{}错误'.format(method))
        # print(res)
        res = self.run_api(url, method, params, headers, cookies)
        print('测试用例执行：{}'.format(res))

        # ---------------------allure报告---------------------------
        # feature（一级标签）：sheet名称
        allure.dynamic.feature(sheet_name)
        # story（二级标签）：模块
        allure.dynamic.story(case_moduel)
        # title：用例ID + 接口名称
        allure.dynamic.title(case_id + case_name)
        # description：请求url，请求类型，预期结果，实际结果，描述……
        desc = "<font color='red'>请求URL</font>：{}\n" \
               "<font color='orange'>请求类型</font>：{}\n" \
               "<font color='green'>预期结果</font>：{}\n" \
               "<font color='blue'>实际结果</font>：{}".format(url, method, expect_result, res)
        allure.dynamic.description(desc)

        # 断言验证
        assert_util = AssertUtil()
        assert_util.assert_code(res['code'], int(code))
        # 验证返回结果内容
        # assert_util.assert_body(res['body'], str(expect_result))

        # 数据库结果断言
        Base.assert_db('db_1', res['body'], db_verify)

    def get_correlation(self, headers, cookies, pre_res):
        """
        处理关联信息
        :param headers:
        :param cookies:
        :param pre_res:
        :return:
        """
        # 验证是否有关联
        headers_para, cookies_para = Base.params_find(headers, cookies)
        # 有关联，执行前置用例，获取结果
        if len(headers_para):
            headers_data = pre_res['body'][headers_para[0]]
            # 结果替换
            headers = Base.res_sub(headers, headers_data)
        if len(cookies_para):
            cookies_data = pre_res['body'][cookies_para[0]]
            # 结果替换
            cookies = Base.res_sub(cookies, cookies_data)
        return headers, cookies


if __name__ == '__main__':
    report_path = conf.get_report_path() + os.sep + 'result'
    report_html_path = conf.get_report_path() + os.sep + 'html'
    pytest.main(['-vs', 'test_case_excel.py', '--alluredir', report_path])
    Base.allure_report(report_path, report_html_path)

    Base.send_mail(title='接口测试报告', content=report_html_path)
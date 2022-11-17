#!/usr/bin/python
# -*- coding: UTF-8 -*-
from config.conf import ConfigYaml
from utils.MysqlUtil import Mysql
import json
import re
from utils.AssertUtil import AssertUtil
from utils.LogUtil import my_log
import subprocess
from utils.EmailUtil import SendEmail


p_data = re.compile('\${(.*)}$')
log = my_log()


# 1、定义init_db
def init_db(db_alais):
    # 2、初始化数据库信息，通过配置文件
    db_info = ConfigYaml().get_db_conf_info(db_alais)
    host = db_info['db_host']
    user = db_info['db_user']
    password = db_info['db_password']
    db_name = db_info['db_name']
    charset = db_info['db_charset']
    port = int(db_info['db_port'])
    # 3、初始化mysql对象
    conn = Mysql(host, user, password, db_name, charset, port)
    print(conn)
    return conn


def assert_db(db_name, result, db_verify):
    assert_util = AssertUtil()
    # 1.初始化数据库
    # sql = init_db('db_1')
    sql = init_db(db_name)
    # # 2.查询sql， excel定义好的
    # if str(db_verify):
    db_res = sql.fetchone(db_verify)
    log.debug('\n数据库查询结果：{}'.format(str(db_res)))
    # 3.数据库的结果与接口返回的结果验证
    # 获取数据库结果中的key
    verify_list = list(dict(db_res).keys())
    # 根据key获取数据库的结果进行验证
    for line in verify_list:
        res_line = result[line]
        res_db_line = dict(db_res)[line]
        # 验证
        assert_util.assert_body(res_line, res_db_line)


def json_parse(data):
    """
    格式化参数，转换为json格式
    :param data:
    :return:
    """
    return json.loads(data) if data else data


def res_find(data, pattern_data=p_data):
    """
    正则表达式查询
    :param data:
    :param pattern_data:
    :return:
    """
    # pattern = re.compile('\${(.*)}$')
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    return re_res


def res_sub(data, replace, pattern_data=p_data):
    """
    正则表达式替换
    :param data:
    :param replace:
    :param pattern_data:
    :return:
    """
    pattern = re.compile(pattern_data)
    re_res = pattern.findall(data)
    if re_res:
        return re.sub(pattern_data, replace, data)
    return data


def params_find(headers, cookies):
    """
    验证请求中是否有${}$需要结果关联
    :param headers:
    :param cookies:
    :return:
    """
    if '${' in headers:
        headers = res_find(headers)
    if '${' in cookies:
        cookies = res_find(cookies)
    return headers, cookies


def allure_report(report_path, report_html):
    """
    生成allure报告
    :param report_path:
    :param report_html:
    :return:
    """
    # 执行命令 allure generate
    allure_cmd = 'allure generate {} -o {} --clean'.format(report_path, report_html)
    log.info('生成报告，地址：')
    try:
        subprocess.call(allure_cmd, shell=True)
    except Exception as ex:
        log.err('生成报告失败，请检查相关配置')
        raise


def send_mail(report_html_path='', content='', title='测试报告'):
    """
    发送邮件
    :param report_html_path:
    :param content:
    :param title:
    :return:
    """
    email_info = ConfigYaml().get_email_info()
    smtp_addr = email_info['smtpserver']
    username = email_info['username']
    password = email_info['password']
    recv = email_info['receiver']
    email = SendEmail(
        smtp_addr=smtp_addr,
        username=username,
        passwd=password,
        recv=recv,
        title=title,
        content=content,
        file=report_html_path)
    email.send_email()


if __name__ == '__main__':
    init_db('db_1')
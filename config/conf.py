#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
from utils.YamlUtil import YamlReader

# 1、获取当前项目的目录
current = os.path.abspath(__file__)
# print(current)
# 获取当前项目的绝对路径
BASE_DIR = os.path.dirname(os.path.dirname(current))
# print(BASE_DIR)

# 定义config目录的路径
_config_path = BASE_DIR + os.sep + 'config'
# 定义data目录的路径
_data_path = BASE_DIR + os.sep + 'data'
# 定义conf.yaml文件的路径
_config_file = _config_path + os.sep + 'conf.yaml'
# 定义db_conf.yaml文件路径
_db_config_file = _config_path + os.sep + 'db_conf.yaml'
# 定义log文件路径
_log_path = BASE_DIR + os.sep + 'logs'

# 定义report文件路径
_report_path = BASE_DIR + os.sep + 'report'

def get_config_path():
    return _config_path

def get_data_path():
    return _data_path

def get_config_file():
    return _config_file

def get_db_config_file():
    return _db_config_file

def get_log_path():
    return _log_path

def get_report_path():
    """
    获取report绝对路径
    :return:
    """
    return _report_path


# 2、读取配置文件
# 创建类
class ConfigYaml:
    # 初始化yaml读取配置文件
    def __init__(self):
        self.config = YamlReader(get_config_file()).data()
        self.db_config = YamlReader(get_db_config_file()).data()

    # 定义方法获取信息
    def get_conf_url(self):
        """
        获取项目测试项目url
        :return:
        """
        return self.config['BASE']['test']['url']

    def get_conf_log(self):
        """
        获取日志级别
        :return:
        """
        return self.config['BASE']['log_level']

    def get_conf_log_extension(self):
        """
        获取日志文件扩展名
        :return:
        """
        return self.config['BASE']['log_extension']

    def get_db_conf_info(self, db_alais):
        """
        根据db_alais获取该数据库的信息
        :param db_alais:
        :return:
        """
        return self.db_config[db_alais]

    def get_excel_file(self):
        """
        获取测试用例文件名称
        :return:
        """
        return self.config['BASE']['test']['case_file']

    def get_excel_sheet(self):
        """
        获取测试用例excel文件sheet名称
        :return:
        """
        return self.config['BASE']['test']['case_sheet']

    def get_email_info(self):
        """
        获取邮件信息
        :return:
        """
        return self.config['email']


if __name__ == '__main__':
    conf_read = ConfigYaml()
    # print(conf_read.get_conf_url())
    # print(conf_read.get_conf_log())
    # print(conf_read.get_conf_log_extension())
    # print(conf_read.get_db_conf_info('db_1'))
    # print(conf_read.get_excel_file())
    # print(conf_read.get_excel_sheet())
    print(conf_read.get_email_info())
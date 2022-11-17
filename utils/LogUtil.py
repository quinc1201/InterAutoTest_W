#!/usr/bin/python
# -*- coding: UTF-8 -*-
import logging
from config import conf
from config.conf import ConfigYaml
import datetime
import os

# 定义日志级别映射
log_l = {
    'info': logging.INFO,
    'debug': logging.DEBUG,
    'warning': logging.WARNING,
    'error': logging.ERROR
}


# 封装Log工具类
# 1、创建类
class Logger:
    # 2、定义参数
    def __init__(self, log_file, log_name, log_level):
        self.log_file = log_file
        self.log_name = log_name
        self.log_level = log_level
        # 3、编写输出控制台或文件
        # 设置logger名称
        self.logger = logging.getLogger(self.log_name)
        # 设置logger级别
        self.logger.setLevel(log_l[self.log_level])
        # 判断handler是否存在
        if not self.logger.handlers:
            # 定义输出格式
            formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
            # 输出到控制台
            fh_stream = logging.StreamHandler()
            fh_stream.setLevel(log_l[self.log_level])
            fh_stream.setFormatter(formatter)
            # 写入文件
            fh_file = logging.FileHandler(self.log_file, encoding='utf-8')
            fh_file.setLevel(log_l[self.log_level])
            fh_file.setFormatter(formatter)
            # 添加handler
            self.logger.addHandler(fh_stream)
            self.logger.addHandler(fh_file)


# 1、初始化参数数据
# 日志文件名称，日志文件级别
# 日志文件名称=logs目录 + 当前时间 + 扩展名
# logs目录
log_path = conf.get_log_path()
# 当前时间
current_time = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
# 扩展名
log_extension = ConfigYaml().get_conf_log_extension()
logfile = os.path.join(log_path, current_time + log_extension)
print(logfile)

# 日志文件级别
loglevel = ConfigYaml().get_conf_log()
# print(loglevel)


# 2、提供对外方法
def my_log(log_name=__file__):
    return Logger(log_file=logfile, log_name=log_name, log_level=loglevel).logger


if __name__ == '__main__':
    my_log().debug("this is a bug")
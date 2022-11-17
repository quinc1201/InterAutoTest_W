#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import yaml


class YamlReader:
    # 判断文件是否存在
    def __init__(self, yaml_file):
        if os.path.exists(yaml_file):
            self.yaml_file = yaml_file
        else:
            raise FileNotFoundError('文件不存在')
        self._data = None
        self._data_all = None

    # 读取单个文档
    def data(self):
        # 第一次调用data()，读取yaml文档，否则直接返回之前保存的数据
        if not self._data:
            with open(self.yaml_file, 'rb') as f:
                self._data = yaml.safe_load(f)
        return self._data

    # 读取多个文档
    def data_all(self):
        # 第一次调用data()，读取yaml文档，否则直接返回之前保存的数据
        if not self._data_all:
            with open(self.yaml_file, 'rb') as f:
                self._data_all = list(yaml.safe_load_all(f))
        return self._data_all

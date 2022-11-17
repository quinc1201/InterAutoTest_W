#!/usr/bin/python
# -*- coding: UTF-8 -*-
from config import conf
import os
from utils.YamlUtil import YamlReader
import pytest
from config.conf import ConfigYaml
from utils.RequestsUtil import Request

# 1、获取测试用例内容list
# 获取testlogin.yaml文件路径
test_file = os.path.join(conf.get_data_path(), 'testlogin.yaml')
# print(test_file)
# 使用工具类来读取多个文档内容
data_list = YamlReader(test_file).data_all()
print(data_list)


# 2、参数化执行测试用例
@pytest.mark.parametrize('login', data_list)
def test_yaml(login):
    # 初始化url，data数据
    url = ConfigYaml().get_conf_url() + login['url']
    # print(url)
    data = login['data']
    # print('data={}'.format(data))
    # post请求
    request = Request()
    res = request.post(url, json=data)
    print(res)


if __name__ == '__main__':
    pytest.main(['-vs', 'atest_login.py'])
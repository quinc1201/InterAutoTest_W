#!/usr/bin/python
# -*- coding: UTF-8 -*-

import yaml

# 读取单个yaml文档
# with open("./data.yaml", encoding='utf-8') as f:
#     r = yaml.safe_load(f)
#     print(r)


# 读取多个yaml文档
# with open('./data2.yaml', encoding='utf-8') as f:
#     r = yaml.safe_load_all(f)
#     for i in r:
#         print(i)

from utils.YamlUtil import YamlReader

res = YamlReader('./data.yaml').data()
print(res)

res2 = YamlReader('./data2.yaml').data_all()
print(res2)
#!/usr/bin/python
# -*- coding: UTF-8 -*-

import yaml


with open("./data.yaml", encoding='utf-8') as f:
    r = yaml.safe_load(f)
    print(r)
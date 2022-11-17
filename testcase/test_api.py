#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from utils.RequestsUtil import requests_get, requests_post
from utils.RequestsUtil import Request
from config.conf import ConfigYaml
from utils.AssertUtil import AssertUtil
from common.Base import init_db


def test_login():
    # url = 'https://api.apiopen.top/api/login'
    conf_y = ConfigYaml()
    url_path = conf_y.get_conf_url()
    url = url_path + '/login'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data = {
        "account": "quincy20221009@outlook.com",
        "password": "ydg123456"
    }
    # r = requests.post(url=url, headers=headers, json=data)
    # print(r.json())
    # r = requests_post(url=url, headers=headers, json=data)
    # print(r)
    request = Request()
    r = request.post(url, headers=headers, data=data)
    print(r)
    code = r['code']
    AssertUtil().assert_code(code, 200)
    body = r['body']
    AssertUtil().assert_in_body(body, '"id": 471')

    # 验证数据库断言
    # 1、初始化数据库对象
    conn = init_db('db_1')
    # 2、查询结果
    res_db = conn.fetchone("select id from user where login_name = 'quincy'")
    print('数据库查询结果={}'.format(res_db))
    # 3、验证
    user_id = res_db['id']
    assert user_id == 11


def get_images():
    url = 'https://api.apiopen.top/api/getImages'
    headers = {
        'accept': 'application/json'
    }
    data = {
        'type': 'beauty',
        'page': 0,
        'size': 10
    }
    r = requests.get(url=url, headers=headers, json=data)
    print(r.json())


def get_video():
    url = 'https://api.apiopen.top/api/getMiniVideo'
    headers = {
        'accept': 'application/json'
    }
    data = {
        'page': 0,
        'size': 10
    }
    # r = requests.get(url=url, headers=headers, params=data)
    # print(r.json())
    # r = requests_get(url, headers, data)
    # print(r)
    request = Request()
    r = request.get(url, headers=headers, json=data)
    print(r)


if __name__ == '__main__':
    # test_login()
    # get_images()
    get_video()

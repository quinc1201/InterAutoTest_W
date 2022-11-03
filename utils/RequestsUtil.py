#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests


# get方法封装
def requests_get(url, headers=None, params=None):
    r = requests.get(url=url, headers=headers, params=params)
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    res = dict()
    res['code'] = code
    res['body'] = body
    return res


# post方法封装
def requests_post(url, headers=None, json=None):
    r = requests.post(url=url, headers=headers, json=json)
    code = r.status_code
    try:
        body = r.json()
    except Exception as e:
        body = r.text
    res = dict()
    res['code'] = code
    res['body'] = body
    return res


# 重构request
class Request:
    def request_api(self, url, data=None, headers=None, method='get'):
        if method == 'get':
            # 执行get请求
            r = requests.get(url=url, headers=headers, params=data)
        elif method == 'post':
            # 执行post请求
            r = requests.post(url=url, headers=headers, json=data)
        # 返回字典
        code = r.status_code
        try:
            body = r.json()
        except Exception as e:
            body = r.text
        res = dict()
        res['code'] = code
        res['body'] = body
        return res

    # 重构get/post方法
    def get(self, url, **kwargs):
        """
        参数
        :param url:
        :param headers:
        :param data:
        :param method:
        :return:
        """
        # 调用公共方法
        return self.request_api(url=url, method='get', **kwargs)

    def post(self, url, **kwargs):
        """
        参数
        :param url:
        :param headers:
        :param data:
        :param method:
        :return:
        """
        # 调用公共方法
        return self.request_api(url=url, method='post', **kwargs)
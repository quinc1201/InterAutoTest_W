#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from utils.LogUtil import my_log


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
    def __init__(self):
        self.log = my_log('Requests')

    def request_api(self, url, json=None, headers=None, cookies=None, method='get'):
        if method == 'get':
            # 执行get请求
            self.log.debug('发送get请求')
            r = requests.get(url=url, headers=headers, params=json, cookies=cookies)
        elif method == 'post':
            # 执行post请求
            self.log.debug('发送post请求')
            r = requests.post(url=url, headers=headers, json=json, cookies=cookies)
        # 返回字典
        # code = r.status_code
        try:
            code = r.json()['code']
            if 'result' in r.json():
                body = r.json()['result']
            else:
                body = r.json()['message']
        except Exception as e:
            code = r.status_code
            body = r.text
            print(e)
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
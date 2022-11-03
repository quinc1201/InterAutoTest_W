#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
from utils.RequestsUtil import requests_get, requests_post
from utils.RequestsUtil import Request


def login():
    url = 'https://api.apiopen.top/api/login'
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
    r = requests.get(url=url, headers=headers, params=data)
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
    r = request.get(url, headers=headers, data=data)
    print(r)


if __name__ == '__main__':
    login()
    # get_images()
    # get_video()

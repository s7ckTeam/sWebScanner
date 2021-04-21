# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/14 18:07
# @Author : 冰海
# @File : get_proxy.py
import re
import random
import requests

from lib.common import add_http
from config.config import Proxy_api, ProxyPool


def random_proxy():
    if Proxy_api:
        proxy = add_http(requests.get(Proxy_api).text)
    elif ProxyPool:
        proxy = add_http(random.choice(ProxyPool))
    else:
        proxy = ""
    regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?])$', re.IGNORECASE)
    proxy = proxy if re.match(regex, proxy) else None
    return proxy
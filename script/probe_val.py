# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 17:29
# @Author : 冰海
# @File : probe_val.py
import os
import time
import json
import random
import asyncio
import aiohttp
import tldextract

from urllib.parse import urljoin
from lib.log import logger
from lib.get_proxy import random_proxy
from lib.common import red_api, Get_Api, IterToAsync, add_http, xre_key, func_key, out_file
from config.config import USER_AGENTS, TimeOut, StatusCode, OS


async def scan_result(url, semaphore, method, params):
    try:
        async with semaphore:
            headers = {
                'User-Agent': random.choice(USER_AGENTS),
                "X-Forwarded-For": random.choice(USER_AGENTS),
                "X-Originating-IP": random.choice(USER_AGENTS),
                "X-Remote-IP": random.choice(USER_AGENTS),
                "X-Remote-Addr": random.choice(USER_AGENTS),
            }
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False),
                                             headers=headers) as session:
                proxy = random_proxy()
                async with session.request(method=method, url=url, proxy=proxy, timeout=TimeOut, verify_ssl=False, **params) as response:
                    status_code = response.status
                    res_json = await response.read()
                    msg = {"url": url, "status_code": status_code, "Content-Length": len(res_json)}
                    if status_code == 200:
                        logger.info(msg)
                    else:
                        logger.warning(msg)
                    return msg

    except Exception as e:
        msg = {"url": url, "status_code": 500, "Content-Length":0}
        logger.error(msg)
        await asyncio.sleep(1)
        return msg


async def read_key(key, semaphore, key_list, func):
    async with semaphore:
        try:
            if key:
                fd = open(key, "r", encoding="utf-8")
                while 1:
                    buffer = fd.read(1024)
                    if not buffer:
                        break
                    result = buffer.split('\n')
                    [key_list.extend(xre_key(res)) for res in result]
            else:
                key_list.extend(func_key(func))
        except:
            logger.error(f"{key}内容读取失败{func}")


async def get_url_list(url_list, api_list, key_list, semaphore):
    async with semaphore:
        async for host in IterToAsync(api_list):
            host = host.strip()
            if host and host[-1] != "/":
                host = host + "/"
            async for key in IterToAsync(key_list):
                key = key.strip()
                if key and key[0] == "/":
                    key = "".join(key[1:])
                subdomain, domain, suffix = tldextract.extract(host)
                url_str = urljoin(host, key)
                if not subdomain and '{SubDomain}' in url_str:
                    url = ""
                elif len(subdomain.split('.')) > 1:
                    for x in tldextract.extract(subdomain):
                        if x:
                            url = url_str.format(Domain='.'.join([subdomain, domain, suffix]).strip('.'),
                                                 SubDomain=subdomain,
                                                 DomainCenter=domain,
                                                 DomainCenterAndTld='.'.join([domain, suffix]).strip('.'))
                else:
                    url = url_str.format(Domain='.'.join([subdomain, domain, suffix]).strip('.'), SubDomain=subdomain,
                                         DomainCenter=domain, DomainCenterAndTld='.'.join([domain, suffix]).strip('.'))
                if url:
                    url_list.append(url)


def asy_main(*args):
    keyword, input_file, url, dict_file, file_type, func, method, params, *_ = args
    logger.info("获取api")
    if input_file:
        api_list = red_api(os.path.abspath(input_file))
    elif keyword:
        api_list = Get_Api(keyword).run()
    else:
        api_list = [add_http(url)]
    logger.info("获取api完成")
    if not api_list:
        logger.error("获取api为空")
        exit()

    if OS == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # 加上这一行处理代理，不能放在协程函数内
    loop = asyncio.get_event_loop()
    semaphore = asyncio.Semaphore(500)

    key_list = []
    loop.run_until_complete(asyncio.wait([read_key(dict_file, semaphore, key_list, func)]))
    key_list = list(set(key_list))
    if not key_list:
        logger.error(f"从{dict_file}获取key为空")
        exit()
    logger.info(f"获取key完成")

    url_list = []
    loop.run_until_complete(asyncio.wait([get_url_list(url_list, api_list, key_list, semaphore)]))
    logger.info(f"获取url_list完成")

    task_list = [scan_result(x, semaphore, method, params) for x in url_list]
    out_file_path = f"out_path/{int(time.time())}/"
    try:
        done, pending = loop.run_until_complete(asyncio.wait(task_list))
        out_file("\n".join([json.dumps(x.result()) for x in done if x.result()['status_code'] in StatusCode]), out_file_path, file_type)
    except RuntimeError:
        pass
    time.sleep(1)
    loop.close()
    logger.info(f"输出文件为: {out_file_path}out_code.{file_type}")


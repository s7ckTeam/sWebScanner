# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 16:56
# @Author : 冰海
# @File : common.py
import os
import re
import xlrd
import json
import base64
import random
import requests
import xlsxwriter

from requests.adapters import HTTPAdapter

from lib.invRegex import all_str
from lib.log import logger
from config.config import USER_AGENTS, Version, fofaApi


def getLatestRevision():
    """
    获取版本信息
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    try:
        req = requests.get(
            url="http://tools.version.weapons.red/tools/Photostudio.txt", headers=headers)
        content = req.text
        readVersion = re.findall(
            "Version\s*=\s*[\"'](?P<result>[\d.]+)", content)
    except:
        readVersion = [Version]

    return readVersion[0]


def red_api(file_path):
    api_list = []
    file_type = file_path.split('.')[-1]
    if file_type in ["xlsx", "xls"]:
        wb = xlrd.open_workbook(file_path)
        for sh in wb.sheets():
            for r in range(sh.nrows):
                domin = sh.row(r)
                api_list.append(add_http(domin))
    elif file_type in ["txt", "csv"]:
        with open(file_path) as f:
            for line in f:
                api_list.append(add_http(line.strip()))
    else:
        logger.warning("不支持文件类型")
    return list(set(api_list))


class Get_Api():

    def __init__(self, ip):
        super(Get_Api, self).__init__()
        self.email = fofaApi['email']
        self.key = fofaApi['key']
        self.headers = {
            "Cache-Control": "max-age=0",
            "User-Agent": random.choice(USER_AGENTS),
            "Upgrade-Insecure-Requests": "1",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.ip = ip

    def run(self):
        keywordsBs = base64.b64encode(self.ip.encode('utf-8'))
        keywordsBs = keywordsBs.decode('utf-8')
        try:
            req = requests.Session()
            req.keep_alive = False
            datas = self.get_data(req, keywordsBs)
            domain_data = list({add_http(x[0]) for x in datas['results']}) if datas else []
            if not domain_data:
                logger.info('获取到的数据为空！')
                exit(0)
            size = len(domain_data)
            data = input(f"获取到 {size} 条数据, 请输入您要扫描的域名数目：")
            try:
                data = int(data)
            except:
                logger.warning('输入不合法')
                exit(0)
            return domain_data[:data]

        except Exception as e:
            logger.error(e)
            return []


    def get_data(self, req, keywordsBs):
        url = f"https://fofa.so/api/v1/search/all?email={self.email}&key={self.key}&qbase64={keywordsBs}&size=10000"
        try:
            req.headers = self.headers
            req.mount("https://", HTTPAdapter(max_retries=2))
            target = req.get(url, timeout=10)
            datas = json.loads(target.text)
            return datas
        except Exception as e:
            logger.error(e)
            return {}


class IterToAsync:
    """普通可迭代对象转异步可迭代对象"""
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value


def is_dir(dirs):
    if not os.path.exists(dirs):
        os.makedirs(dirs)


def out_file(message, dir, file_type):
    is_dir(dir)
    file_name = f"{dir}/out_code.{file_type}"
    if file_type == "json":
        with open(file_name, "w", encoding="utf-8") as f:
            msg = message.replace("\n", ",\n")
            f.write(f"[\n{msg}\n]")
    elif file_type in ["txt", "csv"]:
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(message)
    elif file_type in ["xlsx", "xls"]:
        with xlsxwriter.Workbook(file_name) as workbook:
            worksheet = workbook.add_worksheet('扫描报告')
            bold = workbook.add_format({"bold": True})

            worksheet.set_column('A:A', 30)
            worksheet.set_column('B:B', 30)
            worksheet.set_column('C:C', 30)

            worksheet.write('A1', 'url', bold)
            worksheet.write('B1', 'status_code', bold)
            worksheet.write('C1', 'Content-Length', bold)
            row = 1
            for key in message.split('\n'):
                data = json.loads(key)
                url = data.get("url")
                status_code = data.get("status_code")
                Content_Length = data.get("Content-Length")
                worksheet.write(row, 0, url)
                worksheet.write(row, 1, status_code)
                worksheet.write(row, 2, Content_Length)
                row += 1


def add_http(host):
    return host if "http" in host else f"http://{host}"


def xre_key(key):
    if len(key) >= 3 and key[0] == '%' and key[-1] == "%":
        result = all_str(key[1:-1])
    else:
        result = [key]
    return result


def func_key(key):
    if re.match(r"^\[.+\]\{\d\}$", key):
        result = all_str(key)
    else:
        result = [key]
    return result
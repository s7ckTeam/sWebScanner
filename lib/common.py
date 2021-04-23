# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 16:56
# @Author : 冰海
# @File : common.py
import os
import re
import xlrd
import json
import random
import requests
import xlsxwriter

from lib.invRegex import all_str
from lib.log import logger
from lib.fofa import GetFofaApi
from lib.zoomeye import GetZoomeye
from config.config import USER_AGENTS, Version


def getLatestRevision():
    """
    获取版本信息
    """
    headers = {
        "User-Agent": random.choice(USER_AGENTS),
    }
    try:
        req = requests.get(
            url="http://tools.version.weapons.red/tools/sWebScanner.txt", headers=headers)
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


def Get_Api(api_type, query):
    if api_type == "fofa":
        data = GetFofaApi(query).run()
    elif api_type == "zoomeye":
        data = GetZoomeye(query).run()
    else:
        logger.warning(f"不支持的api类型{api_type}")
        return []
    return data


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
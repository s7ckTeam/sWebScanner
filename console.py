# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 16:53
# @Author : 冰海
# @File : console.py
import random
import argparse

from lib.log import logger
from lib.common import red_api
from lib.update import update
from config.config import pyVersion, Version, Banner, ProxyPool, StatusCode
from script.probe_val import asy_main


def version_check():
    if pyVersion < "3.6":
        logger.error(
            f"此Python版本 ('{pyVersion}') 不兼容,成功运行Screenshot你必须使用版本 >= 3.6 (访问 ‘https://www.python.org/downloads/’)")
        exit(0)


def args_check(cmdparse, usage):
    print(random.choice(Banner))
    confs = {}
    args = []
    if hasattr(cmdparse, "items"):
        cmdlines = cmdparse.items()
    else:
        cmdlines = cmdparse.__dict__.items()
    for key, value in cmdlines:
        confs[key] = value
        args.append(value)
    if confs['version']:
        logger.info(f"Version: {Version}")
        exit(0)
    if confs['updateprogram']:
        update()
        exit(0)
    if ((not confs['query'] or not confs['apitype']) and not confs['file'] and not confs['url']) or (not confs['dict'] and not confs['func']):
        print(usage)
        exit(0)
    if confs['porxy']:
        ProxyPool.extend(red_api(confs['porxy']))
    if confs['code']:
        try:
            StatusCode.extend([int(x) for x in confs['code'].split(",")])
        except:
            print(usage)
            exit(0)
    if confs['params']:
        try:
            kw = {x.split("=")[0]:eval(x.split("=")[1]) for x in confs['params'].split(",")}
            if isinstance(kw, dict):
                params = kw['params'] if 'params' in kw and isinstance(kw['params'], dict) else None
                json = kw['json'] if 'json' in kw and isinstance(kw['json'], dict) else None
                data = kw['data'] if 'data' in kw and isinstance(kw['data'], dict) else None
                args[8] = {'params': params, 'json': json, 'data': data}
        except:
            print(usage)
            exit(0)
    if confs['output'] not in ['json', 'txt', "csv", "xlsx", "xls"]:
        logger.warning(f"暂不支持{confs['output']}文件格式，改为默认文件格式txt输出")
        args[5] = "txt"

    return args


def main():
    version_check()
    parser = argparse.ArgumentParser(description="Screenshot.")
    parser.add_argument('-at', '--apitype', type=str,
                        dest='apitype', help='Input your api type.')
    parser.add_argument('-q', '--query', type=str,
                        dest='query', help='Input your api query.')
    parser.add_argument('-f', '--file', type=str,
                        dest='file', help='Input your api.txt.')
    parser.add_argument('-u', '--url', type=str,
                        dest='url', help='Input your url.')
    parser.add_argument('-d', '--dict', type=str,
                        dest='dict', help='Input your dict file.')
    parser.add_argument('-o', '--output', type=str, default='txt',
                        dest='output', help='output file type.')
    parser.add_argument('-func', '--func', type=str,
                        dest='func', help='Input your rules.')
    parser.add_argument('--method', type=str, default='get',
                        dest='method', help='Input your method.')
    parser.add_argument('--params', type=str, default={},
                        dest='params', help='Input your params.')
    parser.add_argument('--porxy', type=str,
                        dest='porxy', help='Input your porxy file.')
    parser.add_argument('--code', type=str, default='200,403',
                        dest='code', help='Input your code value. 200,403')
    parser.add_argument('-v', '--version', dest='version',
                        action='store_true', help="Show program's version number and exit.")
    parser.add_argument('--update', dest='updateprogram',
                        action='store_true', help="Update the program.")
    args = parser.parse_args()
    usage = f'''
Usage: python3 {parser.prog} -at fofa -q title="admin"
Usage: python3 {parser.prog} -f api.txt
Usage: python3 {parser.prog} -u www.baidu.com
Usage: python3 {parser.prog} ((-at -q) | -f | -u) -d dict.txt
Usage: python3 {parser.prog} ((-at -q) | -f | -u) -func [a-z]{{2}}
Usage: python3 {parser.prog} ((-at -q) | -f | -u) (-d | -func) -o txt
Usage: python3 {parser.prog} ((-at -q) | -f | -u) (-d | -func) --method post
Usage: python3 {parser.prog} ((-at -q) | -f | -u) (-d | -func) --params params={{'your get params': 'value'}},json={{'your post params':'value'}},'data'={{}}
Usage: python3 {parser.prog} ((-at -q) | -f | -u) (-d | -func) --porxy porxy.txt
Usage: python3 {parser.prog} ((-at -q) | -f | -u) (-d | -func) --code 200,403
    '''
    args = args_check(args, usage)
    asy_main(*args)


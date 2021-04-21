# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 15:37
# @Author : 冰海
# @File : sWebScanner.py
import sys
sys.dont_write_bytecode = True

try:
    from lib.log import logger
    import console

    console.main()
except ModuleNotFoundError as ex:
    moduleName = str(ex).split("'")[1]
    logger.error(f"未找到相关模块 {moduleName}")
    logger.info(
        f"输入：python3 -m pip install {moduleName}，或者：pip3 install {moduleName} 进行安装")
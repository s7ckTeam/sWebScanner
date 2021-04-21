# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/12 16:54
# @Author : 冰海
# @File : update.py
import os
import re
import glob
from lib.log import logger
import shutil
import zipfile
import urllib.request
from lib.common import getLatestRevision
from config.config import Version, ZIPBALL_PAGE, GIT_REPOSITORY, BASE_DIR


def update():
    success = False

    if Version == getLatestRevision():
        logger.info("Version：{0} 已经是最新版本".format(Version))
        exit(0)
    elif Version < getLatestRevision():
        logger.info("当前版本 Version: {0}，最新版本为 Version: {1}".format(
            Version, getLatestRevision()))
    else:
        logger.info("Version：{0} 已经是最新版本".format(Version))
        exit(0)
    message = input("是否更新？[y/N]")
    if message == "y":
        directory = os.path.abspath(BASE_DIR)
    else:
        exit(0)
    try:
        open(os.path.join(directory, "sWebScanner.py"), "w+b")
    except Exception as ex:
        logger.error("无法更新目录的内容 '{0}'".format(ex))
    else:
        for wildcard in ('*', "."):
            # glob.glob匹配所有的符合条件的文件，并将其以list的形式返回
            for _ in glob.glob(os.path.join(directory, wildcard)):
                try:
                    if os.path.isdir(_):
                        shutil.rmtree(_)
                    else:
                        os.remove(_)
                except:
                    pass
        if glob.glob(os.path.join(directory, '*')):
            errMsg = "无法清除目录的内容 '{0}'".format(directory)
            logger.error(errMsg)
        else:
            try:
                archive = urllib.request.urlretrieve(ZIPBALL_PAGE)[0]

                with zipfile.ZipFile(archive) as f:
                    for info in f.infolist():
                        info.filename = re.sub(
                            r"sWebScanner-main/", "", info.filename)
                        if info.filename:
                            f.extract(info, directory)

                filepath = os.path.join(BASE_DIR, "config", "config.py")
                if os.path.isfile(filepath):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        nowVersion = re.search(
                            r"(?m)^Version\s*=\s*['\"]([^'\"]+)", f.read()).group(1)
                        logger.info("更新到最新版本：{0}".format(nowVersion))
                        os.remove(archive)
                        success = True
            except Exception as ex:
                logger.error("抱歉！！！更新无法完成 ('{0}')".format(ex))

    if not success:
        logger.info("请前往Github重新下载")
        logger.info("下载地址：{0}".format(GIT_REPOSITORY))
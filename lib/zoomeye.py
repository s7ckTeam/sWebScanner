# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time : 2021/4/22 9:40
# @Author : 冰海
# @File : zoomeye.py
import json
import random
import requests

from requests.adapters import HTTPAdapter

from lib.log import logger
from config.config import USER_AGENTS, zoomeyeApi


class GetZoomeye():
    def __init__(self, ip):
        super(GetZoomeye, self).__init__()
        self.headers = {
            "Cache-Control": "max-age=0",
            "User-Agent": random.choice(USER_AGENTS),
            "Upgrade-Insecure-Requests": "1",
            "API-KEY": zoomeyeApi,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        }
        self.ip = ip


    def run(self):
        if not zoomeyeApi:
            logger.warning("请修改配置文件中zoomeyeApi为您的API-KEY")
            exit(0)
        logger.info("zoomeye数据请求中")
        url = f"https://api.zoomeye.org/host/search?query={self.ip}"
        url_list = []
        try:
            req = requests.Session()
            req.headers = self.headers
            req.mount("https://", HTTPAdapter(max_retries=2))
            target = req.get(url, timeout=10)
            datas = json.loads(target.text)
            if datas.get("matches"):
                url_list.extend(self.get_data(datas.get("matches")))
        except Exception as e:
            logger.error(f"请求失败：{e}")
        return url_list

    def get_data(self, datas):
        url_list = []
        for x in datas:
            ip = x.get("ip")
            portinfo = x.get("portinfo", {})
            port = portinfo.get("port")
            service = portinfo.get("service")
            if ip:
                if port:
                    ip = f"{ip}:{port}"
                if service:
                    ip = f"{service}://{ip}"
                url_list.append(ip)
        return url_list
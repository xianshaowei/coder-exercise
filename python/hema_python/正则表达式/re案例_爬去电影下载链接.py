# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 
   Description :
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019
-------------------------------------------------
   Change Activity:
                   2019
-------------------------------------------------
"""

import os, sys, re
import logging
from logging.handlers import WatchedFileHandler


# 定义日志输出

logfile = __file__ + '.log'
LOGFILE = os.path.expanduser(logfile)
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)  # 控制台中输出DEBUG级别的日志
HANDLER1 = logging.StreamHandler(sys.stdout)
HANDLER2 = WatchedFileHandler(LOGFILE)  # WatchedFileHandler is a kind of filehandler
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s ", "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)  # 日志输出格式
HANDLER2.setFormatter(FMTER)  # 日志输出格式
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)

import requests
import urllib


def log_test():
    LOG.info("test")
    LOG.error("test2")


def get_data(url):
    # ret = urllib.urlopen(url)  # ret = urllib.request.urlopen(url)   #python3.7
    try:
        r = requests.get(url)
    except Exception as e:
        print(e)
        return None
    else:
        if r.status_code not in [200, 201, 204, 206]:
            return None
        print(r.encoding)
        print(r.apparent_encoding)
        print(type(r.text))
        print(type(r.text.encode(r.encoding)))
        encode_content = r.text.encode(r.encoding)
        #encode_content = r.content.encode(r.encoding)
        print(encode_content)
        return encode_content

def get_href(str):

    ret = re.findall(r"<a href=(.*)>(.*)</a><br/>", str)
    if ret:
        # print(ret)
        for i in ret:
            print(i[1])
    else:
        return None


class myclass():

    def __init__(self):
        pass


def main():
    log_test()
    #url = "https://www.ygdy8.net/html/gndy/dyzz/list_23_2.html"
    url = 'https://www.ygdy8.net/html/gndy/dyzz/index.html'
    data = get_data(url)
    get_href(data)


if __name__ == '__main__':
    main()

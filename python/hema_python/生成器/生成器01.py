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

# reload(sys)
# sys.setdefaultencoding("utf-8")

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


def log_test():
    LOG.info("test")
    LOG.error("test2")


class myclass():

    def __init__(self):
        pass






if __name__ == '__main__':
    data_list1 = [x * 2 for x in range(5)]
    for i in data_list1:
        print(i)
    print(data_list1)  # [0, 2, 4, 6, 8]

    # 生成器的创建一

    data_list2 = (x * 2 for x in range(5))
    print(data_list2)  # <generator object <genexpr> at 0x105be25f0>   是一个生成器
    value = next(data_list2)
    print(value)
    value = next(data_list2)
    print(value)

    print("=======================")
    # 生成器的创建二


    def test():
        return 10

    m = test()
    print(m)

    def test1():
        yield 10

    n = test1()
    print(n)

    value = next(n)
    print(value)

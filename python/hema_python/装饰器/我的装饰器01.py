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

#reload(sys)
#sys.setdefaultencoding("utf-8")

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


class myclass(object):

    def __init__(self):
        pass

import time


### 用装饰器实现
def deco(fun):
    def wrapper(*args, **kwargs):
        print("执行装饰器......")
        start_time = time.time()
        fun(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print("time is %d ms" % msecs)
        print("执行装饰器结束......")
    return wrapper


def deco02(fun):
    def wrapper(*args, **kwargs):
        print("执行装饰器02......")
        start_time = time.time()
        fun(*args, **kwargs)
        end_time = time.time()
        msecs = (end_time - start_time) * 1000
        print("time is %d ms" % msecs)
        print("执行装饰器02结束......")
    return wrapper

@deco
def func(a):
    print("hello %s" % a)
    time.sleep(1)

@deco
def func2(a,b):
    print("hello %s,%s" % (a,b))
    time.sleep(1)

@deco02
@deco
def func3(a,b):
    print("hello %s,%s" % (a,b))
    time.sleep(1)
### 用装饰器前
# def add_some_to_func():
#
#     start_time = time.time()
#     func()
#     end_time = time.time()
#     msecs = (end_time - start_time) * 1000
#     print("time is %d ms" % msecs)


def main():
    log_test()
    func("xianwei")
    func2("xian","wei")
    print("")
    func3("xian","wei")

if __name__ == '__main__':
    main()

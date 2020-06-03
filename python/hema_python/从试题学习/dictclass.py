# -*- coding: utf-8 -*-
"""
-------------------------------------------------
 
   Description :
   Author :        xianwei
   Tel :           138 8067 5749
   date：          2019-10-29
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


class dictclass(object):

    def __init__(self, mydict):
        self.mydict = mydict

    def del_dict(self, key):
        if key in self.mydict.keys():
            self.mydict.pop(key)

    def get_dict(self, key):
        if key in self.mydict.keys():
            return self.mydict[key]
        else:
            print("not found.")

    def get_key(self):
        keylist = [k for k in self.mydict.keys()]
        return keylist

    def update_dict(self):

        valuelist = [v for v in self.mydict.values()]
        return valuelist


def main():
    d = dict(zip(['a', 'b', 'c'], [1, 2, 3]))
    print(d)
    myd = dictclass(d)
    print(myd.get_dict('a'))
    myd.del_dict('b')
    print(myd.get_key())
    print(d)
    print(myd.update_dict())


if __name__ == '__main__':
    main()

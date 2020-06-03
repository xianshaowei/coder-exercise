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

reload(sys)
sys.setdefaultencoding("utf-8")


from collections import Iterator



class myclass():

    def __init__(self):
        pass


def main():

    def fibo(n):
        a = b = 1
        index = 0
        while index < n:
            ret = a
            a, b = b, a + b
            index += 1
            print("yield before")
            yield ret  # 执行后，暂停程序，等待next()，只有收到next()信号后才继续推进
            print("next start")  # 收到next()信号后才继续推进

    fi = fibo(5)
    print(fi)
    print(next(fi))  # 1
    print(next(fi))  # 1
    print(next(fi))  # 3
    print(next(fi))  # 5
    print(next(fi))  # 8
    #print(next(fi))  # raise StopIteration


if __name__ == '__main__':
    main()

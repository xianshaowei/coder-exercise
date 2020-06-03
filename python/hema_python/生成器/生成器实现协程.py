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

import time

def work1():
    while True:
        print("work1 正在工作.....")
        yield
        time.sleep(0.5)


def work2():
    while True:
        print("work2 正在工作.....")
        yield
        time.sleep(0.5)


def main():
    w1 = work1()
    w2 = work2()

    i = 0
    while i < 10:
        next(w1)
        next(w2)
        i += 1


if __name__ == '__main__':
    main()

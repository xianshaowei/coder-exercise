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

from collections.abc import Iterator


def main():
    def fibo(n):
        a = b = 1
        index = 0
        while index < n:
            ret = a
            a, b = b, a + b
            index += 1
            print("yield before")
            send_value = yield ret  # 执行后，暂停程序，等待next()，只有收到next()信号后才继续推进
            print("next start")  # 收到next()信号后才继续推进
            if send_value == 555:
                return "send_value == 555，就return啦，让生成器结束....."

    fi = fibo(5)
    print(fi)
    print(next(fi))  # 1

    try:
        print(next(fi))  # 1

        value = fi.send(555)  # 将值传递给生成器中的send_value
        print(value)
    except Exception as e:
        print(e)              # 结果为return返回的值


if __name__ == '__main__':
    main()

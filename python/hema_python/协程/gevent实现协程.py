# -*- coding: utf-8 -*-


import time
import gevent
from gevent import monkey

monkey.patch_all()


def work1():
    while True:
        print("work1 我获取到CPU使用权，可以开始跑啦，哈哈哈.....")
        print("work1 sleep.....")
        # 遇到IO就切换
        print("work1 我后面是IO操作，我要把CPU交出去啦......")
        time.sleep(0.5)  # 需要monkey模块，让gevent识别出是IO操作
        # gevent.sleep(2)
        print("work1 我回来了，继续跑......")


def work2():
    while True:
        print("work2 我获取到CPU使用权，可以开始跑啦，哈哈哈.....")
        print("work2 sleep.....")
        # 遇到IO就切换
        print("work2 我后面是IO操作，我要把CPU交出去啦......")
        time.sleep(0.5)  # 需要monkey模块，让gevent识别出是IO操作
        # gevent.sleep(0.5)
        print("work2 我回来了，继续跑......")


if __name__ == '__main__':
    ge1 = gevent.spawn(work1)
    ge2 = gevent.spawn(work2)

    ge1.join()
    ge2.join()

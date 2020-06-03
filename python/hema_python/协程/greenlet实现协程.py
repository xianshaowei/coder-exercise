# -*- coding: utf-8 -*-


import time
from greenlet import greenlet


def work1():
    while True:
        print("work1 正在工作.....")
        print("work1 sleep.....")
        time.sleep(0.5)
        grt2.switch()  # yield



def work2():
    while True:
        print("work2 正在工作.....")
        print("work2 sleep.....")
        time.sleep(0.5)
        grt1.switch()  # yield


if __name__ == '__main__':
    grt1 = greenlet(work1)
    grt2 = greenlet(work2)

    # 启动
    grt2.switch()



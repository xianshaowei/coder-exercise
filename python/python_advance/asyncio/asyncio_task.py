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

import time
import asyncio

'''
asyncio.ensure_future(coroutine) 和 loop.create_task(coroutine)都可以创建一个task，
run_until_complete的参数是一个futrue对象。
当传入一个协程，其内部会自动封装成task，task是Future的子类。
isinstance(task, asyncio.Future)将会输出True。

'''

class myclass():

    def __init__(self):
        pass


now = lambda: time.time()


async def do_some_work(x):
    print("waiting ... ", x)


def main():
    start = now()

    coroutine1 = do_some_work(2)


    loop = asyncio.get_event_loop()         # 创建一个调度者
    #task1 = loop.create_task(coroutine1)     # 创建一个task
    task2 = asyncio.ensure_future(coroutine1)    # 这种方法也可以创建一个task

    task = task2
    print("task status is ", task)
    loop.run_until_complete(task)           # 将任务加入loop，让调度者处理；
    print("task is ", task)

    end = now()
    print("Time status is ", end - start)



if __name__ == '__main__':
    main()

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
绑定回调，在task执行完毕的时候可以获取执行的结果，
回调的最后一个参数是future对象，通过该对象可以获取协程返回值。
如果回调需要多个参数，可以通过偏函数导入。

'''

class myclass():

    def __init__(self):
        pass


now = lambda: time.time()


async def do_some_work(x):
    print("waiting ... ", x)
    return 'Done after {}s'.format(x)

def callback(furture):
    print('result: ', furture.result())

def main():
    start = now()

    coroutine1 = do_some_work(2)


    loop = asyncio.get_event_loop()         # 创建一个调度者
    task1 = loop.create_task(coroutine1)     # 创建一个task
    task1.add_done_callback(callback)

    task = task1
    print("task status is ", task)
    loop.run_until_complete(task)           # 将任务加入loop，让调度者处理；通过参数future获取协程执行的结果
    print("task is ", task)

    end = now()
    print("Time status is ", end - start)



if __name__ == '__main__':
    main()

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
回调一直是很多异步编程的恶梦，程序员更喜欢使用同步的编写方式写异步代码，
以避免回调的恶梦。回调中我们使用了future对象的result方法。前面不绑定回调的例子中，
我们可以看到task有fiinished状态。在那个时候，可以直接读取task的result方法。

'''

class myclass():

    def __init__(self):
        pass


now = lambda: time.time()


async def do_some_work(x):
    print("waiting ... ", x)
    return 'Done after {}s'.format(x)


def main():
    start = now()

    coroutine1 = do_some_work(2)


    loop = asyncio.get_event_loop()         # 创建一个调度者
    task1 = loop.create_task(coroutine1)     # 创建一个task

    task = task1
    print("task status is ", task)
    loop.run_until_complete(task)           # 将任务加入loop，让调度者处理；通过参数future获取协程执行的结果
    print('task result is : {}'.format(task.result()))
    print("task is ", task)

    end = now()
    print("Time status is ", end - start)



if __name__ == '__main__':
    main()

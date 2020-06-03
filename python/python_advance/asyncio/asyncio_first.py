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
参考： https://www.jianshu.com/p/b5e347b3a17c

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

    loop = asyncio.get_event_loop()
    loop.run_until_complete(coroutine1)


    end = now()
    print("Time is ", end - start)


if __name__ == '__main__':
    main()

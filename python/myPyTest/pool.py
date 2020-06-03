#!/usr/bin/python
# -*- coding: UTF-8 -*-


import time
import os
from multiprocessing import Pool

def func(x):
    time.sleep(1)
    print os.getpid()
    return x*x

def main():
    pool = Pool(processes=4)

    res_list = [ ]
    for i in xrange(4):
        res = pool.apply_async(func,(i,))
        res_list.append(res)
    print res_list
    for i in res_list:
        print i.get()

if __name__ == '__main__':
    main()


# from multiprocessing import Pool
#
#
# class Runner(object):
#     def func(self, i):
#         print i
#         return i
#
#
# runner = Runner()
# pool = Pool(processes=5)
# for i in range(5):
#     pool.apply_async(runner.func, (i, ))
# pool.close()
# pool.join()
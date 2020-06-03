#!/usr/bin/python
# -*- coding: UTF-8 -*-


from multiprocessing import pool
from multiprocessing import Queue
from multiprocessing import process



def myrun(x):
    res = x + 1
    print res
    return res

def mpspool():
    plist = []
    for i in range(20):
        print i
        p = process(target=myrun, args=(i))
        plist.append(p)

    for p in plist:
        p.start()
    for p in plist:
        p.join()


if __name__ == '__main__':
    mpspool()
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
import random
import Queue

reload(sys)
sys.setdefaultencoding("utf-8")

# 定义日志输出

logfile = __file__ + '.log'
LOGFILE = os.path.expanduser(logfile)
LOG = logging.getLogger(__file__)
LOG.setLevel(logging.DEBUG)  # 控制台中输出DEBUG级别的日志
HANDLER1 = logging.StreamHandler(sys.stdout)
HANDLER2 = WatchedFileHandler(LOGFILE)  # WatchedFileHandler is a kind of filehandler
FMTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s]: %(message)s ", "%Y-%m-%d %H:%M:%S")
HANDLER1.setFormatter(FMTER)  # 日志输出格式
HANDLER2.setFormatter(FMTER)  # 日志输出格式
HANDLER1.setLevel(logging.DEBUG)
HANDLER2.setLevel(logging.INFO)
LOG.addHandler(HANDLER1)
LOG.addHandler(HANDLER2)


def log_test():
    LOG.info("test")
    LOG.error("test2")


class ctrlnode():

    def __init__(self, name, mem, cpu):
        self.ctrlName = name
        self.phyMemory = mem
        self.leftMem = self.phyMemory
        self.cpu = cpu
        self.serviceNode = []

    def setLeftMem(self, usemem):
        self.leftMem = self.leftMem - useMem

    def putInService(self, service):
        tmpDict = {service: None}
        self.serviceNode.append(tmpDict)

    def allocatIpToService(self,service,ip):
        for i in range(len(self.serviceNode)):
            for k, v in self.serviceNode[i].iteritems():
                self.serviceNode[i][k] = ip


def getCtrlList(B):
    '''
    一个list类型的bucket,元素为ctrlNode对象
    :return:
    '''
    ctrlList = []
    for k,v in B.iteritems():
        bucket = ctrlnode(k,k['memory'],k['cpu'])
        ctrlList.append(bucket)
    return ctrlList

def getAllCanAllocateMem():
    pass

def main():
    log_test()

    A = {
        "etcd": {'memory': 32, 'cpu': 24, 'num': 2},
        "symsvr": {'memory': 32, 'cpu': 16, "num": 2},
        "apisvr": {'memory': 32, 'cpu': 24, 'num': 2},
        "no": {'memory': 48, 'cpu': 32, 'num': 2},
        "nfvi": {'memory': 48, 'cpu': 32, 'num': 2},
        "nfvisvr": {'memory': 32, 'cpu': 32, 'num': 2},
        "nfc": {'memory': 32, 'cpu': 16, 'num': 1},
        "kmaster": {'memory': 32, 'cpu': 24, 'num': 2},
        "nvc": {'memory': 32, 'cpu': 24, 'num': 2}
    }
    B = {"ctrl1": {'memory': 128, 'cpu': 40},
         "ctrl2": {'memory': 128, 'cpu': 40},
         "ctrl3": {'memory': 128, 'cpu': 40},
         "ctrl4": {'memory': 128, 'cpu': 40},
         "ctrl5": {'memory': 128, 'cpu': 40},
         "ctrl6": {'memory': 128, 'cpu': 40},
         }


    # 总内存是否满足判断
    allMemory = 0

    for k, v in B.items():
        for i, j in v.items():
            if i == 'memory':
                allMemory += j

    leftMemory = allMemory

    # 判断总数是否够
    allNeedMemory = 0
    for k, v in A.items():
        allNeedMemory += v['memory']
    print allNeedMemory

    if allNeedMemory > allMemory:
        raise "Erro,memory of ctrl is not satisfy，pls add ctrl node."
        sys.exit(1)

    print "left memory is %d" % (allMemory - allNeedMemory)

    # 分配机器
    ctrlList = []
    for k, v in B.items():
        k = {}
        ctrlList.append(k)

    # ctrlList 表示包括3个桶的列表
    i = 0
    for k, v in B.items():
        ctrlList[i]['nodeName'] = k
        ctrlList[i]['leftMem'] = v['memory']
        i += 1

    # 生成随机种子列表
    lenList = len(ctrlList)
    #    seedList = [i for i in range(lenList)]
    #    bucketNum = len(ctrlList)
    print'########################################### 过程 ###########################################'
    leftMemoryList = []
    for service, v in A.items():  # 每次取一个service
        seedList = [i for i in range(lenList)]
        for serviceTimes in range(A[service]['num']):  # 根据service的num，确定查找次数
            failTimes = 0
            print service, v, ", Begin to find it ctrl"
            # for i in ctrlList:                              # 开始为service找ctrl节点
            # 随机选ctrl节点

            for j in range(lenList):  # 根据随机种子挑选ctrl节点
                if len(seedList) == 0:
                    # 如果没有找到任何ctrl满足要求
                    print "Error! service: %s , not any ctrl satisfy!" % service
                    raise "Error,not any ctrl node satisfy!"
                ctrlNodeIndex = random.choice(seedList)
                seedList.remove(ctrlNodeIndex)
                # print ctrlNodeIndex

                i = ctrlList[ctrlNodeIndex]
                leftMemory = i['leftMem']
                # 判断ctrl节点是否满足要求
                if service not in i.keys() and A[service]['memory'] < i['leftMem'] and leftMemory > 10:
                    i[service] = 1
                    i['leftMem'] -= A[service]['memory']
                    print "--->OK, %s which ctrl node is %s" % (service, i['nodeName'])
                    break
                else:
                    failTimes += 1

    print'########################################### 结果 ###########################################'
    for i in ctrlList:
        print i

    X = [{'cube': '1'}, {'no': '1'}]
    print len(X)


    # X[0]['cube'] = '2'
    print X
    for k,v in B.iteritems():
        print k,v

if __name__ == '__main__':
    main()

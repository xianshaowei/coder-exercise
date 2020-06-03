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
import queue

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


class ctrlNode():

    def __init__(self, name, mem, cpu):
        self.name = name
        self.phyMemory = mem
        self.leftMem = self.phyMemory
        self.cpu = cpu
        self.serviceNode = []

    def setLeftMem(self, usemem):
        self.leftMem = self.leftMem - useMem

    def putInService(self, service):
        tmpDict = {service: None}
        self.serviceNode.append(tmpDict)

    def allocatIpToService(self, service, ip):
        for i in range(len(self.serviceNode)):
            for k, v in self.serviceNode[i].items():
                self.serviceNode[i][k] = ip


def getCtrlList(ctrlDict):
    '''
    一个list类型的bucket,元素为ctrlNode对象
    :return:
    '''
    ctrlList = []
    for k, v in ctrlDict.items():
        name = k
        ctrl = ctrlNode(name, ctrlDict[k]['memory'], ctrlDict[k]['cpu'])
        ctrlList.append(ctrl)
    return ctrlList


def getAllCanAllocateMem(ctrllist):
    allMemory = 0
    for i in ctrllist:
        allMemory += i.phyMemory
    return allMemory


def getAllNeedMemory(serviceDict):
    allNeedMemory = 0
    for k, v in serviceDict.items():
        allNeedMemory += v['memory']
    print(allNeedMemory)
    return allNeedMemory


def allocatCtrlForService(serviceDict, ctrlList):
    # 生成随机种子列表
    lenList = len(ctrlList)
    print('###################################### 过程 #################################')
    leftMemoryList = []
    for service, v in serviceDict.items():  # 每次取一个service
        seedList = [i for i in range(lenList)]
        for serviceTimes in range(serviceDict[service]['num']):  # 根据service的num，确定查找次数
            print(", Begin to find it ctrl", service, v)
            # for i in ctrlList:                              # 开始为service找ctrl节点
            # 随机选ctrl节点

            for j in range(lenList):  # 根据随机种子挑选ctrl节点
                if len(seedList) == 0:
                    # 如果没有找到任何ctrl满足要求
                    print("Error! service: %s , not any ctrl satisfy!" % service)
                    raise ("Error,not any ctrl node satisfy!")
                ctrlNodeIndex = random.choice(seedList)
                seedList.remove(ctrlNodeIndex)
                # print ctrlNodeIndex

                ctrl = ctrlList[ctrlNodeIndex]
                # 判断ctrl节点是否满足要求
                if service not in ctrl.serviceNode and serviceDict[service][
                    'memory'] < ctrl.leftMem and ctrl.leftMem > 10:
                    ctrl.serviceNode.append({service: '1'})
                    ctrl.leftMem -= serviceDict[service]['memory']
                    print("--->OK, %s which ctrl node is %s" % (service, ctrl.name))
                    break


def allocatIpToCtrlNode(mgrIpQue, storIPQue, ctrlList):
    for ctrl in ctrlList:
        for service in ctrl.serviceNode:
            for k, v in service.items():
                ip = mgrIpQue.get()
                if k == 'no':
                    vip = mgrIpQue.get()
                    noIPList = [ip, vip]
                    service[k] = noIPList
                elif k == 'nfvi':
                    storIP = storIPQue.get()
                    nfviIpList = [ip, storIP]
                    service[k] = nfviIpList
                else:
                    service[k] = ip


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
        "nvc": {'memory': 48, 'cpu': 24, 'num': 2}
    }
    B = {"ctrl1": {'memory': 128, 'cpu': 40},
         "ctrl2": {'memory': 128, 'cpu': 40},
         "ctrl3": {'memory': 128, 'cpu': 40},
         "ctrl4": {'memory': 128, 'cpu': 40},
         "ctrl5": {'memory': 128, 'cpu': 40},
         "ctrl6": {'memory': 128, 'cpu': 40},
         }

    #  将B转换为一个包括ctrlnode对象的list
    ctrlList = getCtrlList(B)

    # 总内存是否满足判断
    allPhyMem = getAllCanAllocateMem(ctrlList)
    allNeedMem = getAllNeedMemory(A)
    print(allNeedMem)
    if allNeedMem > (allPhyMem + len(ctrlList) * 10):
        raise ("Erro,memory of ctrl is not satisfy，pls add ctrl node.")
        sys.exit(1)

    print("##############################")
    allocatCtrlForService(A, ctrlList)

    print('############################## 结果 ###############################')
    # for i in ctrlList:
    #     print(i.name)
    #     print(i.serviceNode)
    #     print(i.leftMem)
    #     print(i.cpu)

    mgrIpQue = queue.Queue()
    mgrIpSegment = '192.168.0.11-150'
    for i in range(11, 150):
        ip = '192.168.0.' + str(i)
        mgrIpQue.put(ip)


    storIpQue = queue.Queue()
    storIpSegment = '192.168.1.11-150'
    for i in range(11, 150):
        ip = '192.168.1.' + str(i)
        storIpQue.put(ip)


    allocatIpToCtrlNode(mgrIpQue, storIpQue, ctrlList)
    # for i in ctrlList:
    #     print(i.name, i.serviceNode, i.leftMem, i.cpu)

    gid = 1060
    normalTag = 1
    for ctrl in ctrlList:
        #print(ctrl.serviceNode)
        for i in ctrl.serviceNode:
            for k, v in i.items():
                print(gid,k,v, ctrl.name, normalTag )
        #for service, ip in ctrl.serviceNode:
        #     print(service, ip)



if __name__ == '__main__':
    main()

#!/usr/bin/python
# -*- coding: UTF-8 -*-


import sys
sys.path.append("..")
import argparse
from pyCommon.color import colorPrint


class test:
    def __init__(self):
        pass

def printip():
    col = colorPrint()
    col.greenPrint("192.168.1.1")


def printip_oneline():
    col = colorPrint()
    col.greenPrint("192.168.1.1 oneline")


def printfile():
    col = colorPrint()
    col.greenPrint("/etc/init.d/networing")


def main():
    # 实例化一个对象
    par = argparse.ArgumentParser(description='Process some integers.')
    # 指定参数
    par.add_argument('--ip', '-i', type=str, help="special a ip")
    # 保存到namespace
    par.add_argument('--oneline', '-o', default=False, help="special a output in oneline", action="store_true")
    par.add_argument('--file', '-f', type=str, help="special a filename")

    # 指定参数
    par.add_argument('--command', '-c', type=str, help="special a command")
    # par.set_defaults(function=sayhi)
    args = par.parse_args()

    # args.function()
    print args

    if args.ip and args.oneline:
        printip_oneline()
    if args.ip and args.oneline == False:
        printip()

    '''
    #python py-test.py  -i 192.168.1.1  -o                                              
    Namespace(command=None, file=None, ip='192.168.1.1', oneline=True)
    192.168.1.1 oneline

    '''


if __name__ == "__main__":
    main()
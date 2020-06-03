#!/usr/bin/python
# -*- coding: UTF-8 -*-

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class colorPrint:
    def __init__(self):
        pass
    def greenPrint(self,*tup):
        '''绿色打印'''
        string = ""
        for i in tup:
            string = string + str(i)
        print ("\033[1;36;40m%s\033[0m") % string

    def redPrint(self,*tup):
        '''红色打印'''
        string = ""
        for i in tup:
            string = string + str(i)
        print ("\033[1;31;40m%s\033[0m") % string

    def fuchsiaPrint(self,*tup):
        '''紫红色打印'''
        string = ""
        for i in tup:
            string = string + str(i)
        print ("\033[1;35;40m%s\033[0m") % string

    def bluePrint(self,*tup):
        '''蓝色打印'''
        string = ""
        for i in tup:
            string = string + str(i)
        print ("\033[1;34;40m%s\033[0m") % string

    def yelloPrint(self,*tup):
        '''黄色打印'''
        string = ""
        for i in tup:
            string = string + str(i)
        print ("\033[1;33;40m%s\033[0m") % string


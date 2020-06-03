#!/usr/bin/python
# -*- coding: UTF-8 -*-


# 测试1，函数中定义函数并返回函数

def hi(name = "cld"):
    def greet():
        print("call function greet()")
    def welcome():
        print("cal function welcome()")

    print name
    if name == 'cld':
        return greet
    else:
        return welcome

print hi()
#<function greet at 0x1055ce8c0>
print hi("h42")
#<function welcome at 0x1055ce938>


print reduce(lambda x, y: x+y, [1, 2, 3, 4, 5])
print (lambda x,y:x+y)(1,2)


# 深拷贝
import copy
I = []
a = {'num': 0}
for i in xrange(3):
    a['num'] = i
    I.append(copy.deepcopy(a))
print I



alist=[1,3,8,10]

less_5_alist = filter(lambda x:x<5,alist)

print less_5_alist


dicta = {'a':1, 'b':2}
dictb = {'a':1, 'c':3}

print dicta.values()
print dictb.values()

set_c = set(dicta.values()).union(set(dictb.values()))
print set_c



def hello():
    print("say hello")

def doSomeBeforeFunc(func):
    print("I am doing some boring work before executing hello()")
    func()

doSomeBeforeFunc(hello)
#结果
#I am doing some boring work before executing hello()
#say hello
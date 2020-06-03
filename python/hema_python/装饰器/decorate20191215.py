# -*- coding: UTF-8 -*-

import time

def fun():
    print("excute fun is {}".format(fun.__name__))

fun()

# 对原函数进行装饰 --- "增强功能"
print("对原函数进行装饰 --- \"增强功能\"")
print("优化1-------------------------------------------------")
def decorate():
    print("loging: begin time is {}".format(time.time()))
    fun()
    print("loging: end time is {}".format(time.time()))

decorate()


# 优化

print("优化2-------------------------------------------------")
def decorate2(func):
    print("loging: begin time is {}".format(time.time()))
    func()
    print("loging: end time is {}".format(time.time()))
    return

decorate2(fun)

print("优化3-------------------------------------------------")
def decorate3(func):
    def wrapper():
        print("loging: begin time is {}".format(time.time()))
        func()
        print("loging: end time is {}".format(time.time()))
        return
    return wrapper


f = decorate3(fun)
f()

print("优化4-------------------------------------------------")
"""
# 新的fun函数名，已经不是原来的函数fun()了，而是功能增强后的fun()
"""
fun = decorate3(fun)
fun()                   # 结果"excute fun is wrapper"


print("优化5---------------------恢复函数名----------------------------")
def fun4():
    print("excute fun is {}".format(fun.__name__))

import functools
def decorate4(func):
    @functools.wraps(func)
    def wrapper():
        print("loging: begin time is {}".format(time.time()))
        func()
        print("loging: end time is {}".format(time.time()))
        return
    return wrapper

fun = decorate4(fun4)
fun()                   # 结果"excute fun is wrapper"

print("优化6---------------------带参数的通用装饰器----------------------------")

import functools
def decorate4(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        print("loging: begin time is {}".format(time.time()))
        func(*args, **kwargs)
        print("loging: end time is {}".format(time.time()))
        return
    return wrapper

@decorate4
def fun5(x):
    print("excute fun is {}, args is {}".format(fun5.__name__, x))

fun5(10)

@decorate4
def fun6(x, y):
    print("excute fun is {}, args is {} and {}".format(fun6.__name__, x, y))

fun6(6,60)

@decorate4
def fun7(intlist):
    print("excute fun is {}, args is {} ".format(fun7.__name__, intlist))

fun7([1, 2 ,3, 4])

# -*- coding: utf-8 -*-


def wapper(fun):
    def infunc(*args, **kwargs):        # 可接受任意参数
        print("---执行权限认证(添加到功能)----")
        ret = fun(*args, **kwargs)      # 可以有返回值
        return  ret
    return infunc

@wapper
def func1():
    print("execution func1")

@wapper
def func2(str):
    print("execution func1, say %s" %str)

@wapper
def func3(str):
    print("execution func3")
    return str

@wapper
def func4(a, b):
    print("execution func4")
    return a+b

func1()
func2("hello")
print(func3("hi"))
print(func4(2,3))



# -*- coding: utf-8 -*-


def outfunc(fun):
    def infunc():
        print("---执行权限认证----")
        print("{name} is {id}".format(name=infunc.__name__, id=id(infunc)) )
        fun()
    return infunc


def func1():
    print("execution func1")


def func2():
    print("execution func2")


# 闭包
funcinstance = outfunc(func1)  # funcinstnace 指向infunc
funcinstance()

# 由闭包到装饰器
# 需要用到新到函数名func1替换原来定义到函数func1()
print(id(func1))  #
func1 = outfunc(func1)  # func1不再是定义的func1()函数，而是一个名字指向infunc
func1()
print("func1 is %d" % id(func1))

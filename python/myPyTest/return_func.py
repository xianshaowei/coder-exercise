# -*- cording: UTF-8 -*-


def func(x):
    def ff(x):
        return 2 * x

    return ff


print(type(func(3)))  # <class 'function'>
f = func(3)
print(f)  # 结果<function func.<locals>.ff at 0x107478268>，说明f是一个函数
print(f(3))  # 6


def sum(*args):
    ax = 0
    print(args)
    for i in args:
        ax = ax + i
    return ax


print(sum(1, 2, 3, 4))

"""
在函数中定义函数

我们在函数lazy_sum中又定义了函数sum，并且，内部函数sum可以引用外部函数lazy_sum的参数和局部变量，
当lazy_sum返回函数sum时，相关参数和变量都保存在返回的函数中，
这种称为“闭包（Closure）”的程序结构拥有极大的威力。

注意： 返回一个函数时，牢记该函数并未执行，返回函数中不要引用任何可能会变化的变量。
"""
def lazy_sum(*args):
    def sum():
        ax = 0
        for i in args:
            ax = ax + i
        return ax

    return sum


f = lazy_sum(1, 3, 5, 7, 9)
res = f()
print(res)          # 25

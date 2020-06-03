# -*- cording: UTF-8 -*-

from functools import partial

# 没有用偏函数情况下
def int2(x, base=2):
    res = int(x, base)
    return res

print(int2('1000'))

# 用偏函数固定第二个参数
f2 = partial(int, base=2)   # 固定参数base=2, 返回一个新的函数
print(f2('1000'))           # 二进制转化为十进制

# 用偏函数固定第二个参数
f8 = partial(int, base=8)   #
print(f8('1000'))           # 八进制转化为十进制
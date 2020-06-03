
"""
@classmethod和@staticmethod 装饰器

"""

class A(object):

    # 定义类属性
    name = 'A'

    # 定义类方法
    @classmethod
    def a(cls):
        print('a')
        print(cls.name)

    def b(self):
        print('b')
        print(self.name)

    # 定义类方法
    @staticmethod
    def c():
        print('c')
        #print(name)        # 错误，不能访问类属性
        #print(self.name)   # 错误，不能访问类属性
        #print(cls.name)    # 错误，不能访问类属性

# 类方法，能直接用类名调用
A.a()

# A.b()  错误，不能用能直接调用方法

obj_A = A()
obj_A.b()   # 普通方法需要用实例调用

# 类方法，能直接用类名调用
A.c()

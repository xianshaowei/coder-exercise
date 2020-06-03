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


class MyList(object):

    def __init__(self):
        self.items = []

    # 对外提供迭代器功能
    def __iter__(self):
        mylist_it = MyIterator(self.items)
        return mylist_it

    def additems(self, item):
        self.items.append(item)

    def print_mylist(self):
        for i in self.items:
            print(i)


class MyIterator(object):

    # 接受传入迭代器的需要迭代的对象
    def __init__(self, items):
        self.items = items
        self.index = 0

    def __iter__(self):
        pass

    # next(iterator)就会调用__next__()方法
    # 注意python2.7没有__next__方法
    def __next__(self):
        if self.index < len(self.items):
            print(self.items[self.index])
            self.index += 1
        else:
            # 停止迭代
            raise StopIteration


def main():
    from collections.abc import Iterable

    mylist = MyList()
    mylist.additems("zhangsan")
    mylist.additems("lishi")
    mylist.additems("wangwu")

    # mylist.print_mylist()

    print(isinstance(mylist, Iterable))

    my_it = iter(mylist)
    print(next(my_it))

    print(next(my_it))

    print(next(my_it))


    for i in mylist:
        print(i)

if __name__ == '__main__':
    main()

# -*- coding: utf-8 -*-

from string import Template

t = Template('${man}folk sed 10yuan to ${otherman}')
d = dict(man='xianwei', otherman='xianduoduo')
#res = t.substitute(d)      # 如果在字典或关键字参数中未提供某个占位符的值，那么 substitute() 方法将抛出 KeyError。
res = t.safe_substitute(d)  # 如果数据缺失，它会直接将占位符原样保留。
print(res)
print(type(res))




# -*- coding: utf-8 -*-

import sys


#sys.path.append('/usr/local/lib/python3.7/site-packages/configobj.py')
print(sys.path)
from configobj import ConfigObj
#
conf_ini = "./test.ini"
config = ConfigObj(conf_ini,encoding='UTF8')
#
# 读配置文件
#
print(config['server'])
print(config['server']['servername'])